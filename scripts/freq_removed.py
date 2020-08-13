import pandas
from matplotlib import pyplot
from matplotlib.ticker import MultipleLocator
import seaborn
# Lists contain a performance metric
# In the case of ops per second, the numbers are unchanged
# In the case of time, its inverse is used

TIKTOK_OFF = [41988.0, 43640.0]
TIKTOK_PART = [35416.0, 37796.0]
TIKTOK_FULL = [34905.39, 36493.69]
TIKTOK_FREQ = [39744.0, 42429.0]
TIKTOK_NOCALLS = [40807.0, 42755.0]


tiktok_off_percent = [100.0] * len(TIKTOK_OFF)
tiktok_part_percent = []
tiktok_on_percent = []
tiktok_freq_removed_percent = []
tiktok_nocalls_percent = []

for i in range(len(TIKTOK_FULL)):
    tiktok_on_percent.append(100.0 * TIKTOK_FULL[i]/ TIKTOK_OFF[i])

for i in range(len(TIKTOK_PART)):
    tiktok_part_percent.append(100.0 * TIKTOK_PART[i]/ TIKTOK_OFF[i])

for i in range(len(TIKTOK_FREQ)):
    tiktok_freq_removed_percent.append(100.0 * TIKTOK_FREQ[i]/ TIKTOK_OFF[i])

for i in range(len(TIKTOK_NOCALLS)):
    tiktok_nocalls_percent.append(100.0 * TIKTOK_NOCALLS[i]/ TIKTOK_OFF[i])


df = pandas.DataFrame({
    'Benchmark': ['Apache Benchmark \nv2.4.29', 'NGINX Benchmark \nv1.9.9'],
    'TikTok Off': tiktok_off_percent,
    'TikTok On - No Calls Protected': tiktok_nocalls_percent,
    'TikTok On - No Writes + Frequent Calls Removed': tiktok_freq_removed_percent,
    'TikTok On - No Writes': tiktok_part_percent,
    'TikTok On': tiktok_on_percent
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