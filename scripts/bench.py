import pandas
from matplotlib import pyplot
from matplotlib.ticker import MultipleLocator
import seaborn
# Lists contain a performance metric
# In the case of ops per second, the numbers are unchanged
# In the case of time, its inverse is used

TIKTOK_OFF = [1/106.46, 2297.33, 1/704.45, 3218980.25, 2493858.67, 1/1001.0, 1/48.79, 42996.0, 43872.61, 3783443.0]
TIKTOK_ON = [1/106.93, 2297.17, 1/705.76, 3168330.33, 2450332.08, 1/1001.0, 1/49.59, 37151.77, 39474.56, 3621268.0]


tiktok_off_percent = [100.0] * len(TIKTOK_OFF)
tiktok_on_percent = []

for i in range(len(TIKTOK_ON)):
    tiktok_on_percent.append(100.0 * TIKTOK_ON[i]/ TIKTOK_OFF[i])


df = pandas.DataFrame({
    'Benchmark': ['Timed Linux \nKernel Compilation \nv5.4', 'OpenSSL v1.1.1 \nRSA 4096-bit', 'Basis Universal \nv1.12 UASTC \nL2 + RDO', 'Redis v5.0.5 \nGET', 'Redis v5.0.5 \nSET', 'PyBench \nv2018-02-16', 'Git', 'Apache Benchmark \nv2.4.29', 'NGINX Benchmark \nv1.9.9', 'IPC TCP 128b'],
    'TikTok OFF': tiktok_off_percent,
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
#pyplot.show()