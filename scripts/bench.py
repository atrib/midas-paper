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

TIKTOK_OFF = [110.41, 2277.0, 3144799.0, 2435308.0, 1002.0, 49.01, 41988.0, 43640.0, 3790028.0]
TIKTOK_PART = [110.9, 2269.0, 3125000.0, 2437066.0, 996.0, 48.62, 35416.0, 37796.0, 3619155.0]
TIKTOK_FULL = [110.41, 2277.2, 3125020.33, 2427298.3, 1001.0, 48.64, 34905.39, 36493.69, 3597080.0]

ERRORS_OFF = [1.84, 16.97, 15045.44, 17192.65, 2.52, 0.19, 233.60, 383.90, 10283.09]
ERRORS_PART = [1.86, 14.69, 0.0, 5231.86, 0.0, 0.39, 184.26, 102.58, 635.34]
ERRORS_FULL = [1.47, 11.24, 5638.27, 11726.17, 0.0, 0.08, 375.15, 35.75 ,3203.20]


tiktok_off_percent = [100.0] * len(TIKTOK_OFF)
tiktok_part_percent = []
tiktok_on_percent = []

for i in range(len(TIKTOK_FULL)):
    tiktok_on_percent.append(100.0 * TIKTOK_FULL[i]/ TIKTOK_OFF[i])
    tiktok_part_percent.append(100.0 * TIKTOK_PART[i]/ TIKTOK_OFF[i])
    ERRORS_OFF[i] *= 100.0/TIKTOK_OFF[i]
    ERRORS_PART[i] *= 100.0/TIKTOK_OFF[i]
    ERRORS_FULL[i] *= 100.0/TIKTOK_OFF[i]


df = pandas.DataFrame({
    'Benchmark': ['Timed Linux \nKernel Compilation \nv5.4*', 'OpenSSL v1.1.1 \nRSA 4096-bit', 'Redis v5.0.5 \nGET', 'Redis v5.0.5 \nSET', 'PyBench \nv2018-02-16*', 'Git*', 'Apache Benchmark \nv2.4.29', 'NGINX Benchmark \nv1.9.9', 'IPC TCP 128b'],
    'TikTok Off': tiktok_off_percent,
    'TikTok Partial': tiktok_part_percent,
    'TikTok Full': tiktok_on_percent
})
seaborn.set_palette('muted')
fig, ax1 = pyplot.subplots(figsize=(8, 4))
tidy = df.melt(id_vars='Benchmark').rename(columns=str.title)
tidy["Errors"] = ERRORS_OFF + ERRORS_PART + ERRORS_FULL
print(tidy)
ax1 = barplot_err(x="Benchmark", y="Value", hue="Variable", data=tidy, ax=ax1, yerr="Errors")
#seaborn.barplot(x='Benchmark', y='Value', hue='Variable', data=tidy, ax=ax1)
seaborn.despine(fig)
seaborn.set_style("whitegrid", {'grid.linestyle': '--'})
#seaborn.set_context("paper")

ax1.yaxis.set_major_locator(MultipleLocator(10))
ax1.grid(True, axis='y')
ax1.tick_params(labelsize=5)
ax1.set_ylabel('TikTok OFF Results [%]')#,fontsize=18)
ax1.set_xlabel('')
pyplot.setp(ax1.get_xticklabels(),  wrap=True)
pyplot.legend(title='', loc="right")
pyplot.savefig("../img/eval.pdf",bbox_inches='tight')
pyplot.show()