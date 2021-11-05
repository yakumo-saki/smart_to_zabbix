import os

def is_not_test_target(filepath):
    base = os.path.basename(filepath)
    return base.startswith("_")
