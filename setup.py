import io
import os

import setuptools

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

NAME = "dashcam_backup"
DESCRIPTION = "Create backup of dashcam data"
AUTHOR = "Brian Haugen"

# check if a VERSION file has been written by the CI, otherwise use dev
VERSION = "0.1.0"
VERSION_FILE = os.path.join(THIS_DIR, "VERSION")
if os.path.exists(VERSION_FILE):
    VERSION = open(VERSION_FILE, "r").read()

REQUIRES_PYTHON = ">=3.11"

# requirements files
REQS_FILE = "./requirements.txt"
if not os.path.exists(REQS_FILE):
    REQS_FILE = "requirements.txt"

# requirements
with open(REQS_FILE, "r") as f:
    REQS = f.read()

try:
    with io.open(os.path.join(THIS_DIR, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setuptools.setup(
    name=NAME,
    version=VERSION,
    packages=setuptools.find_packages(),
    # if you would like to bundle any non-.py files,
    # specify here (ex. test data, markdown, etc.)
    package_data={
        NAME: [
            "tests/*/*",
        ]
    },
    include_package_data=True,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQS,
)
