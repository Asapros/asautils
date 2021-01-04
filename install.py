#
import os
from shutil import copy

try:
    from json import load
    config = load(open("installconfig.json", "r"))
    DIR = config["dir"]
    DISTDIR = config["dist"]
except Exception as e:
    input(e)
    exit()

for module in os.listdir(DIR):
    if module.endswith("py"):
        copy(DIR + module, DISTDIR)
print("Copied module files from %s to %s" % (DIR, DISTDIR))
