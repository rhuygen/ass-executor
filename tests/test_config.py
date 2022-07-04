from pathlib import Path

from ass_executor.config import load_config

HERE = Path(__file__).parent.resolve()


def test_load_config():

    config = load_config(HERE / "data/sample_config.yaml")

    assert "Python Path" in config
    assert "Startup" in config

    assert "script" in config["Startup"]
    assert config["Startup"]["script"] == "~/ass_startup.py"

    assert "prepend" in config["Python Path"]
    assert "append" in config["Python Path"]

    assert config["Python Path"]["append"] == []
    assert config["Python Path"]["prepend"]

    # TODO:
    #  add further tests here for other fields like Apps, Scripts, and Snippets
