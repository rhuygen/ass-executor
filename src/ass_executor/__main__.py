import argparse
import sys

from PyQt5.QtWidgets import QApplication
from executor import ExternalCommand
from .config import load_config
from .gui.view import ASSView
from .gui.control import ASSControl
from .gui.model import ASSModel


# TODO:
#   This function should go into plato-test-scripts with camtest.contingency as module path
def contingency_ui():
    cmd = ExternalCommand("ass-executor --module-path contingency", asynchronous=True)
    cmd.start()


def main():

    parser = argparse.ArgumentParser(prog='ass-executor')
    parser.add_argument('--location', help='location of the Python modules and scripts')
    parser.add_argument('--module-path', help='module path of the Python modules and scripts')

    args = parser.parse_args()

    print(f"{args = }")
    print(f"{args.location = }, {args.module_path = }")

    load_config("ass.yaml")

    app = QApplication([])

    view = ASSView()
    model = ASSModel(args.module_path)
    ASSControl(view, model)

    view.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
