import pandas
from matplotlib import pyplot
from matplotlib.ticker import MultipleLocator
import seaborn
import os
import re
import numpy as np
from collections import defaultdict

full_dir = "omp/full"
par_dir = "omp/par"
off_dir = "omp/off"

def parseData(dir):
    dict_data = defaultdict(list)

    for filename in os.listdir(dir):
        filename_tokens = re.split("\\.|-", filename)
        testname = filename_tokens[0]
        
        
        text_results = open(os.path.join(dir, filename),"r")

        for line in text_results:
            if line.strip().startswith("Time in seconds"):
                line_tokens = line.split()
                dict_data[testname].append(float(line_tokens[4]))

        text_results.close()

    return dict_data


full_dict = parseData(full_dir)
par_dict = parseData(par_dir)
off_dict = parseData(off_dir)


means = {}

for key, value in off_dict.items():
    means[key] = np.mean(value)


new_df = pandas.DataFrame(columns=["Benchmark", "TikTok", "Time"])

for key, value in sorted(off_dict.items()):
    for time in value:
        new_df = new_df.append({"Benchmark":key, "TikTok":"Off", "Time [%]":100.0*time/means[key]}, ignore_index=True)  
  

for key, value in sorted(par_dict.items()):
    for time in value:
        new_df = new_df.append({"Benchmark":key, "TikTok":"Partial", "Time [%]":100.0*time/means[key]}, ignore_index=True)

for key, value in sorted(full_dict.items()):
    for time in value:
        new_df = new_df.append({"Benchmark":key, "TikTok":"Full", "Time [%]":100.0*time/means[key]}, ignore_index=True)
seaborn.set(font_scale=5)
fig, ax1 = pyplot.subplots(figsize=(27, 10))
seaborn.set_style("whitegrid", {'grid.linestyle': '--'})

ax1.grid(True, axis='y')
seaborn.barplot(data=new_df, x="Benchmark", y="Time [%]", hue="TikTok", ax=ax1).set_title("OMP Performance")
ax1.legend().set_title('')
pyplot.show()
