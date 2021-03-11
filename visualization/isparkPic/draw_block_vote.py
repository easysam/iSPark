import pandas as pd
import datetime
import functools
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import matplotlib as mpl
import csv
import numpy as np
mpl.rcParams[u'font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False

register_matplotlib_converters()
plt.set_loglevel("info")

invalid_block = []
all_blocks = pd.read_csv('visualization/isparkPic/occupancy_rate.csv', index_col=0)
for index in all_blocks.index:
    if all_blocks.loc[index].sum() - 0 < 0.01:
        invalid_block.append(index)


def draw_block_vote(block_to_be_draw, version='echart'):
    base_time = datetime.datetime(2018, 9, 3, 10, 30, 00)
    blocks_to_be_drawn = [block_to_be_draw]
    specify_strategy = {'文心四路西侧靠左': [-1 for _ in range(15)] + [0 for _ in range(4)],
                        '海德二道北侧靠左': [-1 for _ in range(15)] + [0 for _ in range(4)],
                        '文心四路东侧靠右': [-1 for _ in range(15)] + [0 for _ in range(4)],
                        '文心三路东侧靠右': [-1 for _ in range(15)] + [0 for _ in range(4)],
                        '文心六路西侧靠左': [-1 for _ in range(15)] + [0 for _ in range(4)],
                        '海德二道南侧靠右': [-1 for _ in range(15)] + [0 for _ in range(4)],
                        '南头街北侧靠左': [-1 for _ in range(15)] + [0 for _ in range(4)],
                        '南头街南侧靠右': [-1 for _ in range(15)] + [0 for _ in range(4)]}
    for item in blocks_to_be_drawn:
        ocean_block = all_blocks.loc[item]
        bcu_sub = [[] for i in range(19)]
        bcu = pd.DataFrame(columns=['time', 'bcu', 'strategy'])
        time_format = "%Y-%m-%d %H:%M:%S"
        for day in range(5):
            use_time = base_time + datetime.timedelta(days=day)
            # print('In', use_time)
            for slot in range(19):
                start_time = use_time + datetime.timedelta(seconds=slot * 1800)
                end_time = start_time + datetime.timedelta(seconds=1800 - 60)
                slot_rates = ocean_block[start_time.strftime(time_format): end_time.strftime(time_format)]
                # print(slot_rates)
                # print(start_time.strftime(time_format),
                #       float(len(slot_rates[slot_rates > 0.85]) - len(slot_rates[slot_rates < 0.7]))/30)
                bcu_sub[slot].append((len(slot_rates[slot_rates > 0.85]) - len(slot_rates[slot_rates < 0.7])) / 30)
        use_time = datetime.datetime(2018, 9, 1, 10, 30, 00)
        for slot in range(19):
            start_time = use_time + datetime.timedelta(seconds=slot * 1800)
            end_time = start_time + datetime.timedelta(seconds=1800 - 60)
            if 'echart' == version:
                start_time = start_time.strftime(time_format)
                end_time = end_time.strftime(time_format)
            if item in specify_strategy:
                strategy = specify_strategy[item][slot]
            else:
                strategy = -1
            bcu = bcu.append({'time': start_time,
                              'bcu': functools.reduce(lambda x, y: x + y, bcu_sub[slot]) / len(bcu_sub[slot]),
                              'strategy': strategy},
                             ignore_index=True)
            bcu = bcu.append({'time': end_time,
                              'bcu': functools.reduce(lambda x, y: x + y, bcu_sub[slot]) / len(bcu_sub[slot]),
                              'strategy': strategy},
                             ignore_index=True)
        # bcu.to_csv('bcu.csv')
        # draw the bcu fig

        fig = Figure(figsize=(4.88, 3.66), tight_layout=True)
        ax = fig.subplots()
        if 'echart' == version:
            print(bcu['time'].tolist())
            return [bcu['time'].tolist(), bcu['bcu'].tolist(), bcu['strategy'].tolist()]
        ax.plot(bcu['time'].tolist(), bcu['bcu'].values, label=u'饱和-闲置平衡指数')
        ax.plot(mdates.date2num(bcu['time'].values), bcu['strategy'].values, label=u'建议定价策略(1:涨价，0：不变，-1：降价)')
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.axhline(-(1. / 3.), color="gray")
        ax.axhline(1. / 3., color='gray')
        blue_line = mlines.Line2D([], [], color='blue', label=u'饱和-闲置平衡指数')
        orange_line = mlines.Line2D([], [], color='orange', label=u'建议定价策略(1:涨价，0：不变，-1：降价)')
        if item in specify_strategy:
            red_patch = mpatches.Patch(color='green', label=u'建议时段10:00~18:00')
            yellow_patch = mpatches.Patch(color='yellow', label=u'建议时段18:00~20:00')
            ax.legend(handles=[red_patch, yellow_patch, blue_line, orange_line], framealpha=0.3)
            ax.axvspan(mdates.date2num(bcu['time'].values)[0], mdates.date2num(bcu['time'].values)[29],
                       facecolor='green', alpha=0.5)
            ax.axvspan(mdates.date2num(bcu['time'].values)[29], mdates.date2num(bcu['time'].values)[37],
                       facecolor='yellow', alpha=0.5)
        else:
            yellow_patch = mpatches.Patch(color='yellow', label=u'建议时段10:00~20:00')
            ax.axvspan(mdates.date2num(bcu['time'].values)[0], mdates.date2num(bcu['time'].values)[37],
                       facecolor='yellow', alpha=0.5)
            ax.legend(handles=[yellow_patch, blue_line, orange_line], framealpha=0.99)
        ax.title.set_text(block_to_be_draw + u' 2018-9-3 至 2018-9-8')
        # plt.axis([mdates.date2num(bcu['time'].values[0] - np.timedelta64(1800, 's')),
        #           mdates.date2num(bcu['time'].values[-1] + np.timedelta64(1800, 's')), -1.1, 1])
        # plt.title(item + ' 2018-9-3 至 2018-9-8')
        # plt.show()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img id='block_vote_pic' src='data:image/png;base64,{data}'/>"


def draw_block_rate(block, draw_datetime, scale, version='echart'):
    rate = []
    if scale == 'avg':
        base_time = datetime.datetime(2018, 9, 3, 1, 0, 0)
        columns = all_blocks.columns.to_series()
        start_time = '2018-09-01 00:05:00'
        end_time = '2018-09-07 23:59:00'
        for i in range(5):
            # count 1 am. to 23 pm. !!!
            iterate_time = base_time + datetime.timedelta(days=1) * i
            start_time = iterate_time.strftime('%Y-%m-%d %H:%M:%S')
            end_time = iterate_time + datetime.timedelta(hours=22)
            end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
            if i == 0:
                for column in columns[start_time: end_time]:
                    rate.append(all_blocks[column][block] / 5)
            else:
                for idx, column in enumerate(columns[start_time: end_time]):
                    rate[idx] += (all_blocks[column][block] / 5)
        if 'echart' == version:
            return [columns[start_time: end_time][::10].tolist(), rate[::10]]
        fig = Figure(figsize=(4.4, 3.3), tight_layout=True)
        ax = fig.subplots()
        ax.plot(pd.to_datetime(columns[start_time: end_time][::10]).values, rate[::10])
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        ax.title.set_text(block + '9月第1周利用率均值')
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f"<img id=\"aggregate_rate\" src='data:image/png;base64,{data}'/>"
    if scale == 'day':
        draw_day = datetime.datetime.strptime(draw_datetime, '%Y-%m-%d %H:%M:%S')
        draw_day = draw_day.replace(hour=0, minute=5, second=0)
        start_time = draw_day.strftime('%Y-%m-%d %H:%M:%S')
        end_time = draw_day + datetime.timedelta(hours=23)
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
    if scale == 'week':
        start_time = '2018-09-01 00:05:00'
        end_time = '2018-09-07 23:59:00'
    columns = all_blocks.columns.to_series()
    for column in columns[start_time: end_time]:
        rate.append(all_blocks[column][block])
    if 'echart' == version:
        return [columns[start_time: end_time][::10].tolist(), rate[::10]]
    fig = Figure(figsize=(4.4, 3.3), tight_layout=True)
    ax = fig.subplots()
    ax.plot(pd.to_datetime(columns[start_time: end_time][::10]).values, rate[::10])
    if scale == 'day':
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        draw_day = datetime.datetime.strptime(draw_datetime, '%Y-%m-%d %H:%M:%S')
        draw_day = draw_day.replace(hour=0, minute=5, second=0)
        draw_day = datetime.datetime.strftime(draw_day, '%Y-%m-%d')
        ax.title.set_text(block + '泊位 ' + draw_day + ' 利用率')
    elif scale == 'week':
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.title.set_text(block + '泊位 2018-9月第一周利用率')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img id=\"block_rate_img\" src='data:image/png;base64,{data}'/>"


def draw_aggregate_rate(draw_datetime, scale):
    aggregate_rate = []
    if scale == 'avg':
        base_time = datetime.datetime(2018, 9, 3, 1, 0, 0)
        columns = all_blocks.columns.to_series()
        start_time = '2018-09-01 00:05:00'
        end_time = '2018-09-07 23:59:00'
        for i in range(5):
            # count 1 am. to 23 pm. !!!
            iterate_time = base_time + datetime.timedelta(days=1) * i
            start_time = iterate_time.strftime('%Y-%m-%d %H:%M:%S')
            end_time = iterate_time + datetime.timedelta(hours=22)
            end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
            if i == 0:
                for column in columns[start_time: end_time]:
                    aggregate_rate.append(all_blocks[column].sum() / (len(all_blocks.index) - len(invalid_block))
                                          / 5)
            else:
                for idx, column in enumerate(columns[start_time: end_time]):
                    aggregate_rate[idx] += (all_blocks[column].sum() / (len(all_blocks.index) - len(invalid_block))
                                            / 5)
        fig = Figure(figsize=(4.4, 3.3), tight_layout=True)
        ax = fig.subplots()
        ax.plot(pd.to_datetime(columns[start_time: end_time][::10]).values, aggregate_rate[::10])
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        ax.title.set_text('南山区 9月第1周 泊位平均利用率均值')
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f"<img id=\"aggregate_rate\" src='data:image/png;base64,{data}'/>"
    if scale == 'day':
        draw_day = datetime.datetime.strptime(draw_datetime, '%Y-%m-%d %H:%M:%S')
        draw_day = draw_day.replace(hour=0, minute=5, second=0)
        start_time = draw_day.strftime('%Y-%m-%d %H:%M:%S')
        end_time = draw_day + datetime.timedelta(hours=23)
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
    if scale == 'week':
        start_time = '2018-09-01 00:05:00'
        end_time = '2018-09-07 23:59:00'
    columns = all_blocks.columns.to_series()
    for column in columns[start_time: end_time]:
        aggregate_rate.append(all_blocks[column].sum() / (len(all_blocks.index) - len(invalid_block)))
    fig = Figure(figsize=(4.4, 3.3), tight_layout=True)
    ax = fig.subplots()
    ax.plot(pd.to_datetime(columns[start_time: end_time][::10]).values, aggregate_rate[::10])
    if scale == 'day':
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        draw_day = datetime.datetime.strptime(draw_datetime, '%Y-%m-%d %H:%M:%S')
        draw_day = draw_day.replace(hour=0, minute=5, second=0)
        draw_day = datetime.datetime.strftime(draw_day, '%Y-%m-%d')
        ax.title.set_text('南山区' + draw_day + '泊位平均利用率')
    elif scale == 'week':
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.title.set_text('南山区 2018-9-3 至 2018-9-8 泊位平均利用率')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img id=\"aggregate_rate\" src='data:image/png;base64,{data}'/>"


def sum_up_pie(all_block, congestion_block, underuse_block, balance_block):
    fig = Figure(figsize=(4.4, 3.3), tight_layout=True)
    ax = fig.subplots()
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = '饱和', '平衡', '闲置'
    sizes = [int(congestion_block), int(balance_block), int(underuse_block)]
    explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img id=\"aggregate_rate\" src='data:image/png;base64,{data}'/>"

def get_data_of_all_block(draw_datetime, scale):
    aggregate_rate = []
    if scale == 'avg':
        base_time = datetime.datetime(2018, 9, 3, 1, 0, 0)
        columns = all_blocks.columns.to_series()
        start_time = '2018-09-01 00:05:00'
        end_time = '2018-09-07 23:59:00'
        for i in range(5):
            # count 1 am. to 23 pm. !!!
            iterate_time = base_time + datetime.timedelta(days=1) * i
            start_time = iterate_time.strftime('%Y-%m-%d %H:%M:%S')
            end_time = iterate_time + datetime.timedelta(hours=22)
            end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
            if i == 0:
                for column in columns[start_time: end_time]:
                    aggregate_rate.append(all_blocks[column].sum() / (len(all_blocks.index) - len(invalid_block))
                                          / 5)
            else:
                for idx, column in enumerate(columns[start_time: end_time]):
                    aggregate_rate[idx] += (all_blocks[column].sum() / (len(all_blocks.index) - len(invalid_block))
                                            / 5)
        fig = Figure(figsize=(4.4, 3.3), tight_layout=True)
        ax = fig.subplots()
        ax.plot(pd.to_datetime(columns[start_time: end_time][::10]).values, aggregate_rate[::10])
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        ax.title.set_text('南山区 9月第1周 泊位平均利用率均值')
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        # return [pd.to_datetime(columns[start_time: end_time][::10]).values.tolist(), aggregate_rate[::10]]
        return [columns[start_time: end_time][::10].tolist(), aggregate_rate[::10]]
    if scale == 'day':
        draw_day = datetime.datetime.strptime(draw_datetime, '%Y-%m-%d %H:%M:%S')
        draw_day = draw_day.replace(hour=0, minute=5, second=0)
        start_time = draw_day.strftime('%Y-%m-%d %H:%M:%S')
        end_time = draw_day + datetime.timedelta(hours=23)
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
    if scale == 'week':
        start_time = '2018-09-01 00:05:00'
        end_time = '2018-09-07 23:59:00'
    columns = all_blocks.columns.to_series()
    for column in columns[start_time: end_time]:
        aggregate_rate.append(all_blocks[column].sum() / (len(all_blocks.index) - len(invalid_block)))
    return [columns[start_time: end_time][::10].tolist(), aggregate_rate[::10]]
def getRecentUsed(road_name):
    dictroadnumber = dict() #存储number与路段名对应关系
    with open("visualization/isparkPic/newinfo73.csv", "r", encoding="utf-8-sig") as csvreader:
        csv_reader = csv.reader(csvreader)
        for row in csv_reader:
           number = row[0]
           road = row[1]
           dictroadnumber[road] = number
    ##横坐标设置
    timesplot = []
    base_time = datetime.datetime(2018, 10, 20, 10, 00, 00)
    for i in range(10):
        iterate_time = base_time + datetime.timedelta(hours = 1*i)
        #start_time = iterate_time.strftime('%Y-%m-%d %H:%M:%S')
        start_time = iterate_time.strftime('%H:%M')
        timesplot.append(start_time)
    #data设置
    as_data = np.load('visualization/isparkPic/prediction.npz')
    prediction = as_data['prediction']
    ground_truth = as_data['ground']


    road_number =  int(dictroadnumber[road_name])
    pred_data = []
    true_data = []
    for i in range(0,10):
        pred_data.append(sum(prediction[i][road_number])/len(prediction[i][road_number]))
        true_data.append(sum(ground_truth[i][road_number])/len(ground_truth[i][road_number]))
    #print(pred_data)
    #print(true_data)
    return [timesplot,pred_data,true_data]




