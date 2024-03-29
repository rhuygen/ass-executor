from .model import ASSModel
from .view import ASSView


class ASSControl:
    def __init__(self, view: ASSView, model: ASSModel):
        self._view = view
        self._model = model

        self._modules = self._model.get_ui_modules()

        self._funcs = self._model.get_ui_buttons_functions(self._modules["ui_test_script"])

        self._view.add_function_button(self._funcs["func_with_args"])
