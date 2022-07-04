from src.ass_executor.gui.model import ASSModel
from src.ass_executor.gui.view import ASSView


class ASSControl:
    def __init__(self, view: ASSView, model: ASSModel):
        self.view = view
        self.model = model
