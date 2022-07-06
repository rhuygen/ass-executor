from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List
from typing import Tuple

from executor import ExternalCommand
from executor import ExternalCommandFailed

from ass_executor.utils import expand_path


class CommandError(Exception):
    pass


class Command:
    def __init__(self, name: str, path: Path = None, python_path: str = None, category: str = None, args: List[str] = None):
        self._name = name
        self._path = path
        self._category = category
        self._args = args
        self._python_path = python_path or ""

        self._parsed_args = None

    def execute(self, capture: bool = True, asynchronous: bool = True) -> str | Command:
        return ""

    def can_execute(self) -> bool:
        return self._parsed_args is not None

    def set_python_path(self, python_path: str):
        # TODO:
        #    proper checking of the format of python_path
        self._python_path = python_path

    def get_python_path(self) -> str:
        return self._python_path

    def get_required_args(self) -> List[Tuple[str, str]]:
        """
        Returns a list with the required arguments and their expected types.
        """
        required_args = []
        for arg_name, arg_text in self._args:
            if m := re.search(r"<<([:\w]+)>>", arg_text):
                match = m[1]
                name, expected_type = match.split(':') if ':' in match else (match, None)
                required_args.append((name, expected_type))
        return required_args

    def parse_args(self, **kwargs):
        """
        Parses the arguments list and for each input request it will ask for input. When all input has been received
        the full argument list is constructed and returned as a string.

        Args:
            **kwargs: list of input arguments

        Returns:
            A string containing all arguments
        """
        parsed_args = ""
        for arg_name, arg_text in self._args:
            if m := re.search(r"<<([:\w]+)>>", arg_text):
                x, *_ = m[1].split(':')
                arg_value = kwargs[x] if x in kwargs else input(f"Enter a value for {x}: ")
            elif arg_text == "None":
                arg_value = ""
            else:
                arg_value = arg_text
            parsed_args += f"{arg_name} {arg_value} "

        self._parsed_args = parsed_args.strip()


class AppCommand(Command):
    def __init__(self, name: str, app_name: str):
        super().__init__(name)
        self._app_name = app_name


class ScriptCommand(Command):
    """This class represents a script command, i.e. a Python scripts which is executed as such."""
    def __init__(self, name: str, script_name: str, path: Path = None, python_path: str = None, category: str = None, args: List[str] = None):
        super().__init__(name, path=path, python_path=python_path, category=category, args=args)
        self._script_name = script_name
        self._cmd: ExternalCommand | None = None

    @staticmethod
    def from_config(config, name: str) -> ScriptCommand:
        from ass_executor.config import ASSConfiguration, ConfigError
        config: ASSConfiguration

        if "Scripts" not in config:
            raise ConfigError(f"No scripts defined in the configuration '{config.name}'")

        if name not in config.get_script_names():
            raise ConfigError(f"No script definition found for '{name}' in the configuration '{config.name}'.")

        python_path = config.get_python_path()
        script: dict = config["Scripts"][name]
        script_name = script.get("script_name")
        path = script.get("path")
        category = script.get("category")
        args = script.get("args")

        return ScriptCommand(name, script_name, path=path, python_path=python_path, category=category, args=args)

    def execute(self, capture: bool = True, asynchronous: bool = False) -> None:
        cmd_line = self.get_command_line()
        python_path = self.get_python_path()

        self._cmd = ExternalCommand(f"PYTHONPATH={python_path} {cmd_line}", capture=capture, capture_stderr=True, asynchronous=asynchronous)
        try:
            self._cmd.start()
        except ExternalCommandFailed as exc:
            raise CommandError(self._cmd.error_message) from exc

    def is_running(self) -> bool:
        return self._cmd.is_running if self._cmd is not None else False

    def get_output(self) -> str:
        return self._cmd.output if self._cmd is not None else ""

    def get_error(self) -> str:
        return self._cmd.error_message

    def get_command_line(self) -> str:
        path = expand_path(self._path)
        if not path.exists():
            raise CommandError(f"The path '{self._path}' was expanded into '{path}' which doesn't exist.")

        filepath = path / self._script_name
        if not filepath.exists():
            raise CommandError(f"The generated filepath '{filepath}' doesn't exit for command script {self._name}")

        return f"{sys.executable} {filepath} {self._parsed_args}"


class SnippetCommand(Command):
    def __init__(self, name: str):
        super().__init__(name)
