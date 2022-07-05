import os

from ass_executor.utils import replace_environment_variable


def test_replace_environment_variable():

    assert replace_environment_variable("PLAIN_STRING") == "PLAIN_STRING"

    assert replace_environment_variable("~/data/CSL") == "~/data/CSL"

    os.environ["DATA_STORAGE_LOCATION"] = "/Users/rik/data/CSL"
    assert replace_environment_variable("ENV['DATA_STORAGE_LOCATION']") == "/Users/rik/data/CSL"

    os.environ["DATA_STORAGE_LOCATION"] = "/Users/rik/data"
    assert replace_environment_variable("ENV['DATA_STORAGE_LOCATION']/CSL") == "/Users/rik/data/CSL"
