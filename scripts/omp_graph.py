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


all_data = {"FULL":{}, "PART":{}, "OFF":{}}

for key, value in off_dict.items():
    all_data["OFF"][key] = np.mean(value)

for key, value in full_dict.items():
    all_data["FULL"][key] = np.mean(value)/all_data["OFF"][key]

for key, value in par_dict.items():
    all_data["PART"][key] = np.mean(value)/all_data["OFF"][key]

for key, value in off_dict.items():
    all_data["OFF"][key] = 1.00

df = pandas.DataFrame(all_data)
new_df = pandas.DataFrame(columns=["Benchmark", "TikTok", "Time"])


for i in range(len(df.values)):
    for j in range(len(df.values[i])):
        new_df = new_df.append({"Benchmark":df.axes[0][i], "TikTok":df.axes[1][j], "Time":df.values[i][j]}, ignore_index=True)

fig, ax1 = pyplot.subplots(figsize=(27, 10))
seaborn.set_style("whitegrid", {'grid.linestyle': '--'})

ax1.grid(True, axis='y')
seaborn.barplot(data=new_df, x="Benchmark", y="Time", hue="TikTok", ax=ax1).set_title("OMP Performance")
pyplot.show()
