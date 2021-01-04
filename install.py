#
import os
from shutil import copy

print("[install.py] Setting up...")
try:
    from json import load
    config = load(open("installconfig.json", "r"))
    DIR = config["dir"]
    DISTDIR = config["dist"]
    GITBRANCH = config["branch"]
except Exception as e:
    input(e)
    exit()

print("[install.py] Copying modules...")
modules = []
for module in os.listdir(DIR):
    if module.endswith("py"):
        copy(DIR + module, DISTDIR)
        modules.append(module)
print("[install.py] Copied module files from %s to %s" % (DIR, DISTDIR))
print("[install.py] Pushing to git...")
for module in modules:
    os.system("git add %s" % module)
os.system("git checkout %s" % GITBRANCH)
os.system("git commit -m \"Automatic commit \"")
os.system("git push origin %s" % GITBRANCH)
print("[install.py] Pushed to branch %s" % GITBRANCH)
