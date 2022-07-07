from pathlib import Path

from ass_executor.config import load_config
from ass_executor.utils import remove_ansi_escape

HERE = Path(__file__).parent.resolve()


def test_print_sys_path_as_script():

    config = load_config(HERE / "data/snippets.yaml")

    cmd = config.get_command_for_snippet("print sys.path script")

    cmd.execute()

    out = cmd.get_output()

    print()
    print(f"*****\n{out = }\n*****")

    assert "Python.framework" in remove_ansi_escape(out)
    assert "Python.framework" in out


def test_print_sys_path_as_snippet():

    config = load_config(HERE / "data/snippets.yaml")

    cmd = config.get_command_for_snippet("print sys.path code")

    cmd.execute()

    out = cmd.get_output()

    print()
    print(f"*****\n{out = }\n*****")

    assert "Python.framework" in remove_ansi_escape(out)
    assert "Python.framework" in out
