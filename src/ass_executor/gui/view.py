from typing import Callable

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton

from .exec import get_arguments


class DynamicButton(QPushButton):
    def __init__(self, label: str, func: Callable):
        super().__init__(label)
        self._function = func

    @property
    def function(self):
        return self._function

class ASSView(QMainWindow):
    def __init__(self):
        super().__init__()
        self._button = None
        self.setWindowTitle("Contingency GUI")

    def add_function_button(self, func: Callable):
        print(f"Creating a button for {func.__name__ = }")

        self._button = DynamicButton(func.__name__, func)
        self._button.clicked.connect(self.the_button_was_clicked)
        self.setCentralWidget(self._button)

    def the_button_was_clicked(self, *args, **kwargs):

        print(f"{args = }, {kwargs = }")

        # TODO
        #   This should be done from the control or model and probably in the background?

        ui_args = get_arguments(self._button.function)

        args = [23, 42]

        print(self._button.function(*args))
