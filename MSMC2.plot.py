#! /usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys


mu = 1.25e-8
gen = 2
dir_ = "MSMC2_OUPUT"

msmc_output = pd.read_csv(sys.argv[1], sep = "\t", header = 0)
t_years = gen * ((msmc_output.left_time_boundary + msmc_output.right_time_boundary)/2) / mu

plt.figure(figsize = (8, 10))
plt.semilogx(t_years, (1/msmc_output.lambda1)/(2*mu), drawstyle = "steps", color = "red", label = "DE")

plt.xlabel("years age")
plt.ylabel("population Sizes")
plt.legend()
plt.savefig("DE.MSMC.pdf")

