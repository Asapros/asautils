#
import os
from shutil import copy
import time


start = time.time()
print("Setting up...")
try:
    from json import load
    config = load(open("installconfig.json", "r"))
    DIR = config["dir"]
    DISTDIR = config["dist"] + "asautils//"
except Exception as e:
    input(e)
    exit()

print("Copying modules...")
for module in os.listdir(DIR):
    if module.endswith(".py"):
        try:
            copy(DIR + module, DISTDIR)
        except (FileNotFoundError, PermissionError) as e:
            input(e)
            exit()
print("Copied module files from %s to %s" % (DIR, DISTDIR))
input("Completed in " + str(time.time() - start))
