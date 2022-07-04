import sys

from PyQt5.QtWidgets import QApplication

from .config import load_config
from .gui.view import ASSView
from .gui.control import ASSControl
from .gui.model import ASSModel


def main():

    args = list(sys.argv)

    load_config("ass.yaml")

    app = QApplication(args)

    view = ASSView()
    model = ASSModel()
    ASSControl(view, model)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
