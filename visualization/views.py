from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .models import OccupancyList, BerthBelong, BlocksCapacity, RoadShape, RoadList
import json
import decimal
import logging
from datetime import datetime
from datetime import timedelta
import os
import pickle
from .isparkPic import draw_block_vote as draw

logging.basicConfig(level=logging.DEBUG)


class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)


def index(request):
    if 'datetime' not in request.POST:
        request_time = '2018-09-01 11:30:00'
    elif (datetime.strptime(request.POST['datetime'], '%Y-%m-%d %H:%M:%S') > datetime(2018, 9, 7, 23, 59, 59)
          or datetime.strptime(request.POST['datetime'], '%Y-%m-%d %H:%M:%S') < datetime(2018, 9, 1, 0, 5, 0)):
        request_time = '2018-09-01 11:30:00'
    else:
        request_time = request.POST['datetime']
    # block_info = list(BlocksCapacity.objects.all().values())
    rs = list(RoadShape.objects.all().values('id', 'block', 'shape'))
    query = 'SELECT `blocks_capacity`.`block_id`, ifnull(A.berth_count, 0) as used_count,' \
            '       `blocks_capacity`.`capacity`, `blocks_capacity`.`road`, `blocks_capacity`.`left_or_right`,' \
            '       `blocks_capacity`.`direction` ' \
            'FROM  blocks_capacity ' \
            'LEFT outer JOIN (' \
            '   SELECT `block_id`, COUNT(`berth`) as berth_count FROM `berth_belong` ' \
            '   WHERE `berth`in (' \
            '       SELECT `berthage` ' \
            '       FROM `occupancy_list` ' \
            '       WHERE `in_time`< \'' + request_time + '\' and out_time > \'' + request_time + '\'' \
            '   ) GROUP by `block_id`' \
            ')as A ' \
            'on `blocks_capacity`.block_id= A.block_id'
    occupancy = BlocksCapacity.objects.raw(query)
    block_info = dict()
    for record in occupancy:
        block_info[record.block_id] = dict()
        block_info[record.block_id]['used_count'] = record.used_count
        block_info[record.block_id]['road_name'] = record.road
        block_info[record.block_id]['capacity'] = record.capacity
        block_info[record.block_id]['left_or_right'] = record.left_or_right
        block_info[record.block_id]['direction'] = record.direction
        block_info[record.block_id]['occupancy_rate'] = float(record.used_count) / float(record.capacity)
        if block_info[record.block_id]['occupancy_rate'] > 0.9:
            block_info[record.block_id]['color'] = 'red'
        elif block_info[record.block_id]['occupancy_rate'] < 0.8:
            block_info[record.block_id]['color'] = 'blue'
        else:
            block_info[record.block_id]['color'] = 'green'
        block_info[record.block_id]['shape'] = list()
    for shape in rs:
        block_info[int(shape['block'])]['shape'].append(shape['shape'])
    for road in list(block_info):
        if len(block_info[road]['shape']):
            continue
        if block_info[road]['used_count']:
            logging.error('lack shape data ' + block_info[road]['road_name'])
            return
        block_info.pop(road)
    return render(request, 'visualization/index.html',
                  {'block_info': sorted(block_info.items()), 'datetime': request_time})


def echarts(request):
    return render(request, 'visualization/e_index.html')

def get_aggregate_rates_data(request):
    return HttpResponse(json.dumps(draw.get_data_of_all_block(request.GET['datetime'], request.GET['data_scale']), cls=DjangoJSONEncoder))
# Create your views here.
def edit(request):
    if 'road_name' in request.POST and 'left_or_right' in request.POST and 'direction' in request.POST:
        block = get_object_or_404(BlocksCapacity, road=request.POST['road_name'],
                                  left_or_right=request.POST['left_or_right'], direction=request.POST['direction'])
        rs = RoadShape.objects.filter(block=block.block_id).values('id', 'shape')
        return render(request, 'visualization/map_adjustment.html', {'block_info': block, 'shape': list(rs)})
    else:
        return render(request, 'visualization/map_adjustment.html', {'block_info': 'null', 'shape': []})


def save_path_info(request):
    if request.method == 'POST':
        logging.debug('save_path_info: ', request.POST)
        if 'block_id' in request.POST:
            print(request.POST.get('road_info'))
            rs = RoadShape(block=request.POST.get('block_id'), shape=request.POST.get('road_info'))
            rs.save()
            return HttpResponse('success')  # if everything is OK
        # nothing went well
    return HttpResponse('FAIL!!!!!')


def test(request):
    if 'page_date' in request.POST:
        request_time = request.POST['page_date'] + ' ' + request.POST['page_time']
    else:
        if 'datetime' not in request.POST:
            request_time = '2018-09-01 11:30:00'
        elif (datetime.strptime(request.POST['datetime'], '%Y-%m-%d %H:%M:%S') > datetime(2018, 9, 7, 23, 59, 59)
              or datetime.strptime(request.POST['datetime'], '%Y-%m-%d %H:%M:%S') < datetime(2018, 9, 1, 0, 5, 0)):
            request_time = '2018-09-01 11:30:00'
        else:
            request_time = request.POST['datetime']
    # block_info = list(BlocksCapacity.objects.all().values())
    rs = list(RoadShape.objects.all().values('id', 'block', 'shape'))
    query = 'SELECT `blocks_capacity`.`block_id`, ifnull(A.berth_count, 0) as used_count,' \
            '       `blocks_capacity`.`capacity`, `blocks_capacity`.`road`, `blocks_capacity`.`left_or_right`,' \
            '       `blocks_capacity`.`direction` ' \
            'FROM  blocks_capacity ' \
            'LEFT outer JOIN (' \
            '   SELECT `block_id`, COUNT(`berth`) as berth_count FROM `berth_belong` ' \
            '   WHERE `berth`in (' \
            '       SELECT `berthage` ' \
            '       FROM `occupancy_list` ' \
            '       WHERE `in_time`< \'' + request_time + '\' and out_time > \'' + request_time + '\'' \
            '   ) GROUP by `block_id`' \
            ')as A ' \
            'on `blocks_capacity`.block_id= A.block_id'
    occupancy = BlocksCapacity.objects.raw(query)
    block_info = dict()
    berth_used_count = 0
    for record in occupancy:
        block_info[record.block_id] = dict()
        block_info[record.block_id]['used_count'] = record.used_count
        block_info[record.block_id]['road_name'] = record.road
        block_info[record.block_id]['capacity'] = record.capacity
        block_info[record.block_id]['left_or_right'] = record.left_or_right
        block_info[record.block_id]['direction'] = record.direction
        block_info[record.block_id]['occupancy_rate'] = float(record.used_count) / float(record.capacity)
        berth_used_count += record.used_count
        if block_info[record.block_id]['occupancy_rate'] > 0.9:
            block_info[record.block_id]['color'] = 'red'
        elif block_info[record.block_id]['occupancy_rate'] < 0.8:
            block_info[record.block_id]['color'] = 'blue'
        else:
            block_info[record.block_id]['color'] = 'green'
        block_info[record.block_id]['shape'] = list()
    for shape in rs:
        block_info[int(shape['block'])]['shape'].append(shape['shape'])
    avg_occupancy = 0
    block_count = 0
    berth_count = 0
    for road in list(block_info):
        if len(block_info[road]['shape']):
            avg_occupancy += block_info[road]['occupancy_rate']
            block_count += 1
            berth_count += block_info[road]['capacity']
            continue
        if block_info[road]['used_count']:
            logging.error('lack shape data ' + block_info[road]['road_name'])
            return
        block_info.pop(road)
    avg_occupancy /= block_count
    page_date = request_time[:10]
    page_time = request_time[11:]
    print(request_time)
    return render(request, 'visualization/test.html',
                  {'block_info': sorted(block_info.items()), 'datetime': request_time, 'page_date': page_date, 'page_time': page_time, 'avg_occupancy': round(avg_occupancy*100), 'used_proportion': round(float(berth_used_count)/float(berth_count)*100),
                   'unused_proportion': round((1 - float(berth_used_count)/float(berth_count))*100)}, )


def road_loc(request):
    roads = RoadList.objects.all().values('road', 'longitude', 'latitude')
    return render(request, 'visualization/road_loc_show.html', {'roads': roads})


def delete_seg(request):
    RoadShape.objects.filter(pk=request.POST['seg_id']).delete()
    return HttpResponse('yes')


def miss_price(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, './ns_miss_price_rates.py3')
    with open(file_path, 'rb') as f:
        miss_prices = pickle.load(f)
    rs = list(RoadShape.objects.all().values('id', 'block', 'shape'))
    block_info = dict()
    for shape in rs:
        if int(shape['block']) not in block_info:
            block_info[int(shape['block'])] = dict()
            block_info[int(shape['block'])]['shape'] = list()
            if miss_prices[int(shape['block'])] == 0:
                block_info[int(shape['block'])]['color'] = 'Navy'
            elif miss_prices[int(shape['block'])] < 0.1:
                block_info[int(shape['block'])]['color'] = 'Blue'
            elif miss_prices[int(shape['block'])] < 0.2:
                block_info[int(shape['block'])]['color'] = 'RoyalBlue'
            elif miss_prices[int(shape['block'])] < 0.3:
                block_info[int(shape['block'])]['color'] = 'DodgerBlue'
            elif miss_prices[int(shape['block'])] < 0.4:
                block_info[int(shape['block'])]['color'] = 'DeepSkyBlue'
            elif miss_prices[int(shape['block'])] < 0.5:
                block_info[int(shape['block'])]['color'] = 'MediumSpringGreen'
            elif miss_prices[int(shape['block'])] < 0.6:
                block_info[int(shape['block'])]['color'] = 'GreenYellow'
            elif miss_prices[int(shape['block'])] < 0.7:
                block_info[int(shape['block'])]['color'] = 'Yellow'
            elif miss_prices[int(shape['block'])] < 0.8:
                block_info[int(shape['block'])]['color'] = 'Gold'
            elif miss_prices[int(shape['block'])] < 0.9:
                block_info[int(shape['block'])]['color'] = 'OrangeRed'
            else:
                block_info[int(shape['block'])]['color'] = 'red'
        block_info[int(shape['block'])]['shape'].append(shape['shape'])
    for road in list(block_info):
        if len(block_info[road]['shape']):
            continue
        if block_info[road]['used_count']:
            logging.error('lack shape data ' + block_info[road]['road_name'])
            return
        block_info.pop(road)
    return render(request, 'visualization/index.html', {'block_info': sorted(block_info.items())})


def use_rank(request):
    if request.GET['rank'] == 'use':
        query = 'SELECT A.`block_id`, ifnull(B.berth_count, 0) as used_count, A.`capacity`, ifnull(B.berth_count, 0)/A.`capacity` as rate, ifnull(B.berth_count, 0), A.`capacity`, A.`road`, A.`left_or_right`, A.`direction` ' \
                'FROM ' \
                '(SELECT `block_id`, `capacity`, `road`, `left_or_right`, `direction` FROM blocks_capacity WHERE `district`=\'南山区\') as A ' \
                'LEFT outer JOIN ' \
                '(SELECT `block_id`, COUNT(`berth`) as berth_count FROM `berth_belong` WHERE `berth`in (SELECT `berthage` FROM `occupancy_list` WHERE `in_time`< \'' + \
                request.GET['datetime'] + '\' and out_time > \'' + request.GET[
                    'datetime'] + '\') GROUP by `block_id`) as B ' \
                                  'on A.block_id= B.block_id ' \
                                  'ORDER BY `rate` desc'
    else:
        query = 'SELECT A.`block_id`, ifnull(B.berth_count, 0) as used_count, A.`capacity`, ifnull(B.berth_count, 0)/A.`capacity` as rate, ifnull(B.berth_count, 0), A.`capacity`, A.`road`, A.`left_or_right`, A.`direction` ' \
                'FROM ' \
                '(SELECT `block_id`, `capacity`, `road`, `left_or_right`, `direction` FROM blocks_capacity WHERE `district`=\'南山区\') as A ' \
                'LEFT outer JOIN ' \
                '(SELECT `block_id`, COUNT(`berth`) as berth_count FROM `berth_belong` WHERE `berth`in (SELECT `berthage` FROM `occupancy_list` WHERE `in_time`< \'' + \
                request.GET['datetime'] + '\' and out_time > \'' + request.GET[
                    'datetime'] + '\') GROUP by `block_id`) as B ' \
                                  'on A.block_id= B.block_id ' \
                                  'ORDER BY `rate` asc'
    occupancy = BlocksCapacity.objects.raw(query)
    block_used_info = list()
    for record in occupancy:
        temp_info = dict()
        temp_info['block_id'] = record.block_id
        temp_info['used_count'] = record.used_count
        temp_info['road_name'] = record.road
        temp_info['capacity'] = record.capacity
        temp_info['left_or_right'] = record.left_or_right
        temp_info['direction'] = record.direction
        temp_info['occupancy_rate'] = record.rate
        block_used_info.append(temp_info)
    return HttpResponse(json.dumps(block_used_info, cls=DjangoJSONEncoder, ensure_ascii=False))


def block_vote(request):
    # print(request)
    # print(request.GET['block_id'], request.GET['road_name'], request.GET['direction'], request.GET['left_or_right'],
    #       request.GET['datetime'])
    block_to_be_draw = ''.join((request.GET['road_name'], request.GET['direction'], request.GET['left_or_right']))
    data_buffer = draw.draw_block_vote(block_to_be_draw, version=request.GET['version'])
    return_value = json.dumps(data_buffer, cls=DjangoJSONEncoder)

    return HttpResponse(return_value)


def aggregate_rates(request):
    print('aggregate', request.GET)
    return HttpResponse(draw.draw_aggregate_rate(request.GET['datetime'], request.GET['data_scale']))


def block_rate(request):
    block_to_be_draw = ''.join((request.GET['road_name'], request.GET['direction'], request.GET['left_or_right']))
    rate_data = draw.draw_block_rate(block_to_be_draw, request.GET['datetime'], request.GET['scale'], request.GET['version'])
    return HttpResponse(json.dumps(rate_data))


def parking_proportion_and_future(request):
    interval = timedelta(minutes=15)
    base_time = datetime.strptime(request.GET['datetime'], '%Y-%m-%d %H:%M:%S')
    proportion_amount = []
    for i in range(4):
        query_time = base_time - interval * pow(2, i)
        query_time = query_time.strftime('%Y-%m-%d %H:%M:%S')
        query = 'SELECT `berth` FROM `berth_belong` WHERE `block_id`= ' + str(
            request.GET['block_id']) + ' AND `berth` IN( ' \
                                       '       SELECT `berthage` ' \
                                       '       FROM `occupancy_list` ' \
                                       '       WHERE `in_time`< \'' + query_time + '\' and `out_time` > \'' + \
                request.GET['datetime'] + '\')'
        occupancy = BerthBelong.objects.raw(query)
        if i == 0:
            proportion_amount.append(int(request.GET['occupied']) - len(occupancy))
        else:
            proportion_amount.append((int(request.GET['occupied']) - len(occupancy)) - sum(proportion_amount))
    proportion_amount.append(len(occupancy))
    response = '''
                <table class="table table-sm">
                  <thead>
                    <tr>
                      <th scope="col">已停车时长</th>
                      <th scope="col">数量</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th scope="row">0~15分</th>
                      <td>''' + str(proportion_amount[0]) + '''</td>
                    </tr>
                    <tr>
                      <th scope="row">15~30分</th>
                      <td>''' + str(proportion_amount[1]) + '''</td>
                    </tr>
                    <tr>
                      <th scope="row">30分~1时</th>
                      <td colspan="2">''' + str(proportion_amount[2]) + '''</td>
                    </tr>
                    <tr>
                      <th scope="row">1~2时</th>
                      <td colspan="2">''' + str(proportion_amount[3]) + '''</td>
                    </tr>
                    <tr>
                      <th scope="row">大于2时</th>
                      <td colspan="2">''' + str(proportion_amount[4]) + '''</td>
                    </tr>
                  </tbody>
                </table>'''
    query_time = base_time + timedelta(hours=1)
    query_time = query_time.strftime('%Y-%m-%d %H:%M:%S')
    query = 'SELECT `berth` FROM `berth_belong` WHERE `block_id`= ' + str(request.GET['block_id']) \
            + ' AND `berth` IN( ' \
              '       SELECT `berthage` ' \
              '       FROM `occupancy_list` ' \
              '       WHERE `in_time`< \'' + query_time + '\' and `out_time` > \'' + query_time + '\')'
    occupancy = BerthBelong.objects.raw(query)
    response += '<span class="font-italic">一小时后预测占用率：' \
                + str(int(round(len(occupancy) / int(request.GET['capacity']) * 100, 0))) + '%</span>'
    return HttpResponse(response)


def draw_sum_up_pie(request):
    return HttpResponse(draw.sum_up_pie(request.GET['all_block'], request.GET['congestion_block'],
                                        request.GET['underuse_block'], request.GET['balance_block']))
def draw_road_predict(request):

    pre_true_data = draw.getRecentUsed(request.GET['road_name'])
    print(pre_true_data)
    return HttpResponse(json.dumps(pre_true_data))
