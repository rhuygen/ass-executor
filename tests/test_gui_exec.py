import sys
from pathlib import Path

from ass_executor.gui.exec import exec_ui
from ass_executor.gui.exec import find_ui_button_functions

HERE = Path(__file__).parent.resolve()


def test_exec_ui():

    @exec_ui()
    def press():
        return "Pressed"

    assert hasattr(press, "__UI_BUTTON__")
    assert press() == "Pressed"


def test_ui_script():

    print()

    sys.path.insert(0, str(HERE))  # make sure Python knows where to look for the module

    funcs = find_ui_button_functions("contingency.ui_test_script")

    print(f"{funcs = }")

    assert funcs[0][0] == "concatenate_args"
    assert funcs[0][1]("one", "two") == "onetwo"
