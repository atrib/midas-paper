import pandas
from matplotlib import pyplot
from matplotlib.ticker import MultipleLocator
import seaborn

def barplot_err(x, y, xerr=None, yerr=None, data=None, **kwargs):

    _data = []
    for _i in data.index:

        _data_i = pandas.concat([data.loc[_i:_i]]*3, ignore_index=True, sort=False)
        _row = data.loc[_i]
        if xerr is not None:
            _data_i[x] = [_row[x]-_row[xerr], _row[x], _row[x]+_row[xerr]]
        if yerr is not None:
            _data_i[y] = [_row[y]-_row[yerr], _row[y], _row[y]+_row[yerr]]
        _data.append(_data_i)

    _data = pandas.concat(_data, ignore_index=True, sort=False)

    _ax = seaborn.barplot(x=x,y=y,data=_data,ci='sd',**kwargs)

    return _ax


# Lists contain a performance metric
# In the case of ops per second, the numbers are unchanged
# In the case of time, its inverse is used

TIKTOK_OFF = [41988.0, 43640.0]
TIKTOK_PART = [35416.0, 37796.0]
TIKTOK_FULL = [34905.39, 36493.69]
TIKTOK_FREQ = [39744.0, 42429.0]
TIKTOK_NOCALLS = [40954.0, 42660.0]

ERRORS_OFF = [233.60, 383.90]
ERRORS_PART = [184.26, 102.58]
ERRORS_FULL = [375.15, 35.75]
ERRORS_FREQ = [311.22, 234.64]
ERRORS_NOCALLS = [453.04,153.64]

tiktok_off_percent = [100.0] * len(TIKTOK_OFF)
tiktok_part_percent = []
tiktok_on_percent = []
tiktok_freq_removed_percent = []
tiktok_nocalls_percent = []

for i in range(len(TIKTOK_FULL)):
    tiktok_on_percent.append(100.0 * TIKTOK_FULL[i]/ TIKTOK_OFF[i])
    ERRORS_FULL[i] /= TIKTOK_OFF[i]
    ERRORS_FULL[i] *= 100.0

for i in range(len(TIKTOK_PART)):
    tiktok_part_percent.append(100.0 * TIKTOK_PART[i]/ TIKTOK_OFF[i])
    ERRORS_PART[i] /= TIKTOK_OFF[i]
    ERRORS_PART[i] *= 100.0

for i in range(len(TIKTOK_FREQ)):
    tiktok_freq_removed_percent.append(100.0 * TIKTOK_FREQ[i]/ TIKTOK_OFF[i])
    ERRORS_FREQ[i] /= TIKTOK_OFF[i]
    ERRORS_FREQ[i] *= 100.0

for i in range(len(TIKTOK_NOCALLS)):
    tiktok_nocalls_percent.append(100.0 * TIKTOK_NOCALLS[i]/ TIKTOK_OFF[i])
    ERRORS_NOCALLS[i] /= TIKTOK_OFF[i]
    ERRORS_NOCALLS[i] *= 100.0

for i in range(len(TIKTOK_OFF)):
    ERRORS_OFF[i] /= TIKTOK_OFF[i]
    ERRORS_OFF[i] *= 100.0

errors = ERRORS_OFF + ERRORS_NOCALLS + ERRORS_FREQ + ERRORS_PART + ERRORS_FULL

df = pandas.DataFrame({
    'Benchmark': ['Apache Benchmark \nv2.4.29', 'NGINX Benchmark \nv1.9.9'],
    'TikTok Off': tiktok_off_percent,
    'No Calls': tiktok_nocalls_percent,
    'Frequent Whitelisted': tiktok_freq_removed_percent,
    'No Writes': tiktok_part_percent,
    'TikTok On': tiktok_on_percent
})
seaborn.set(font_scale=1)
fig, ax1 = pyplot.subplots(figsize=(4, 2))
tidy = df.melt(id_vars='Benchmark').rename(columns=str.title)

tidy["Errors"] = errors

ax1 = barplot_err(x="Benchmark", y="Value", hue="Variable", data=tidy, ax=ax1, yerr="Errors")
#seaborn.barplot(x='Benchmark', y='Value', hue='Variable', data=tidy, ax=ax1)
seaborn.despine(fig)
seaborn.set_style("whitegrid", {'grid.linestyle': '--'})
seaborn.set_context("paper")



#ax1.yaxis.set_major_locator(MultipleLocator(10))
ax1.grid(True, axis='y')
#ax1.tick_params(labelsize=15)
ax1.set_ylabel('TikTok OFF Performance [%]')
ax1.set_xlabel('')
pyplot.setp(ax1.get_xticklabels(),  wrap=True)
pyplot.legend(title='')
pyplot.savefig("../img/freq_removed.pdf",bbox_inches='tight')
pyplot.show()