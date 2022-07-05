import time
from pathlib import Path

from executor import ExternalCommand

from ass_executor.config import load_config

HERE = Path(__file__).parent.resolve()


def test_script_execution():

    config = load_config(HERE / "data/long_running_command_config.yaml")

    cmd = config.get_command_for_script("Long Running Command")

    args = cmd.get_required_args()
    assert ('duration', 'int') in args

    duration = 2
    cmd.parse_args(duration=duration)

    if cmd.can_execute():
        cmd.execute()

    cmd_line = cmd.get_command_line()
    assert f"--duration {duration}" in cmd_line

    cmd = ExternalCommand(cmd_line, capture=True, asynchronous=True)
    cmd.start()

    cmd.wait()
    # while cmd.is_running:
    #     time.sleep(1)

    assert f"sleep({duration}).." in cmd.output
