import pandas
from matplotlib import pyplot
from matplotlib.ticker import MultipleLocator
import seaborn
# Lists contain a performance metric
# In the case of ops per second, the numbers are unchanged
# In the case of time, its inverse is used

TIKTOK_OFF = [1/110.41, 2277.0, 3144799.0, 2435308.0, 1/1002.0, 1/49.01, 41988.0, 43640.0, 3790028.0]
TIKTOK_PART = [1/110.9, 2269.0, 3125000.0, 2437066.0, 1/996.0, 1/48.62, 35416.0, 37796.0, 3619155.0]
TIKTOK_FULL = [1/110.41, 2277.2, 3125020.33, 2427298.3, 1/1001.0, 1/48.64, 34905.39, 36493.69, 3597080.0]


tiktok_off_percent = [100.0] * len(TIKTOK_OFF)
tiktok_part_percent = []
tiktok_on_percent = []

for i in range(len(TIKTOK_FULL)):
    tiktok_on_percent.append(100.0 * TIKTOK_FULL[i]/ TIKTOK_OFF[i])

for i in range(len(TIKTOK_PART)):
    tiktok_part_percent.append(100.0 * TIKTOK_PART[i]/ TIKTOK_OFF[i])


df = pandas.DataFrame({
    'Benchmark': ['Timed Linux \nKernel Compilation \nv5.4', 'OpenSSL v1.1.1 \nRSA 4096-bit', 'Redis v5.0.5 \nGET', 'Redis v5.0.5 \nSET', 'PyBench \nv2018-02-16', 'Git', 'Apache Benchmark \nv2.4.29', 'NGINX Benchmark \nv1.9.9', 'IPC TCP 128b'],
    'TikTok OFF': tiktok_off_percent,
    'TikTok PART': tiktok_part_percent,
    'TikTok ON': tiktok_on_percent
})
fig, ax1 = pyplot.subplots(figsize=(27, 10))
tidy = df.melt(id_vars='Benchmark').rename(columns=str.title)
seaborn.barplot(x='Benchmark', y='Value', hue='Variable', data=tidy, ax=ax1)
seaborn.despine(fig)
seaborn.set_style("whitegrid", {'grid.linestyle': '--'})
seaborn.set_context("paper")

ax1.yaxis.set_major_locator(MultipleLocator(10))
ax1.grid(True, axis='y')
ax1.tick_params(labelsize=15)
ax1.set_ylabel('TikTok OFF Performance',fontsize=15)
ax1.set_xlabel('')
pyplot.setp(ax1.get_xticklabels(),  wrap=True)
pyplot.legend(title='', fontsize=15, loc="right")
pyplot.savefig("../img/eval.pdf",bbox_inches='tight')
pyplot.show()