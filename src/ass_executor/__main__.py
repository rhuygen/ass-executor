import sys

from PyQt5.QtWidgets import QApplication

from src.ass_executor.gui.view import ASSView
from src.ass_executor.gui.control import ASSControl
from src.ass_executor.gui.model import ASSModel


def main():

    args = list(sys.argv)

    app = QApplication(args)

    view = ASSView()
    model = ASSModel()
    ASSControl(view, model)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
