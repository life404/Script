#! /usr/bin/env python3

import sys
import argparse
import subprocess
import os

path = os.path.join("/disk/panda2bat/La_io/04.GeneFamily/05.positive.selection/04.codmel/OG0010020","Ma", "mlc")
print(path)
command = " ".join(["grep", "-w", "\"lnL\"", path])
print(command)
result = subprocess.run(command, shell = True, stdout = subprocess.PIPE, encoding = "utf-8")
print(result.stdout.split(" "))
print(result.returncode)
