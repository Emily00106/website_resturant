# Path configurations

import pathlib


ROOT = pathlib.Path(__file__).parent

TEMPLATES_PATH = ROOT.joinpath("application/templates")
TEXT_PATH = ROOT.joinpath("application/static/text")
