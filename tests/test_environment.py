from pathlib import Path

from ass_executor.config import load_config

HERE = Path(__file__).parent.resolve()


def test_check_environment_for_script():

    config = load_config(HERE / "data/scripts.yaml")

    cmd = config.get_command_for_script("Check Environment")
    cmd.execute()
    cmd.get_output()


def test_check_environment_for_snippet():

    config = load_config(HERE / "data/snippets.yaml")

    cmd = config.get_command_for_snippet("Check Environment")
    cmd.execute()
    cmd.get_output()

    assert cmd.get_error() is None
