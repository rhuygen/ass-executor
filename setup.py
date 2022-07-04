import contextlib
import os
import pathlib
import sys
from shutil import rmtree

from setuptools import setup, Command

# Package meta-data.

NAME = "ass-executor"
PACKAGE_NAME = "ass_executor"
DESCRIPTION = "Apps, Scripts, and Snippets = ASS Executor."
URL = "https://github.com/rhuygen/ass-executor"
EMAIL = "rik.huygen@kuleuven.be"
AUTHOR = "Rik Huygen"
REQUIRES_PYTHON = '>=3.8.0'
VERSION = None

# The directory containing this file

HERE = pathlib.Path(__file__).parent

# The directory containing the source code

SRC = HERE / "src"

# The text of the README file

README = (HERE / "README.md").read_text()

# Load the package's __version__.py module as a dictionary.

about = {}
if VERSION is None:
    with open(os.path.join(SRC, PACKAGE_NAME, '__version__.py')) as f:
        exec(f.read(), about)
        VERSION = about['__version__']


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package to PyPI.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        with contextlib.suppress(OSError):
            self.status('Removing previous builds…')
            rmtree(os.path.join(HERE, 'dist'))
        self.status("Building Source and Wheel (universal) distribution…")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel --universal")

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system(f"git tag v{VERSION}")
        os.system('git push --tags')

        sys.exit()


# This call to setup() does all the work

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Utilities",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["ass_executor", "ass_executor.gui"],
    package_dir={"": "src"},
    package_data={"": ["textualog.png", "examples/*.log"]},
    include_package_data=False,
    install_requires=["rich", "PyQt5"],
    entry_points={
        "gui_scripts": [
            "ass-executor=ass_executor.__main__:main",
        ]
    },
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
