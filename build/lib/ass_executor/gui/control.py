from .model import ASSModel
from .view import ASSView


class ASSControl:
    def __init__(self, view: ASSView, model: ASSModel):
        self.view = view
        self.model = model
