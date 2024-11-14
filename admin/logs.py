import copy
import datetime
import json
import logging
from functools import partial

from pywebio import config
from pywebio.output import put_text, use_scope, put_table, put_button, popup, put_row
from pywebio.pin import put_input, pin
from pywebio.session import set_env

from admin.header import navbar
from admin.statis import statis
from mongodb_utils import search_last_logs


@config(title="日志")
def main():
    set_env(output_max_width='80%')
    navbar()
    # 输入框
    put_row([put_text("过滤器：").style('text-align: right; font-size: 1.2em; margin-top: 5px'),
             put_input('filter', value='{}'),
             put_button('查询', onclick=query_logs).style('margin-left: 5px')], size="100px 400px 80px")
    query_logs()


def query_logs():
    try:
        filter_json = json.loads(pin.filter)
    except Exception as e:
        filter_json = {}
        logging.error(f"json: {pin.filter}, 解析错误: {e}")
    get_all_logs(filter_json)


def show_detail(log):
    popup(f"日志详情: {log['log_type']}", [
        put_text(f"{log}"),
    ])


def get_all_logs(filter_json):
    logs = search_last_logs(filter_json, 100)
    rows = []
    for log in logs:
        log_type = log['log_type']
        # log['uuid']不存在返回""
        uuid = ""
        if log.get('uuid'):
            uuid = log['uuid']
        time = ""
        if log.get('time'):
            time = log['time']
        create_at = ""
        if log.get('create_at'):
            create_at = log['create_at']
            try:
                dt = datetime.datetime.fromtimestamp(create_at)
                create_at = dt.strftime('%Y-%m-%d %H:%M:%S.%f')
            except Exception as e:
                logging.error(f"时间转换错误: {e}")

        ip = ""
        if log.get('ip'):
            ip = log['ip']
        param = copy.deepcopy(log)
        del param['_id']
        del param['log_type']
        del param['uuid']
        del param['ip']
        del param['time']
        del param['create_at']

        # 按钮弹窗显示log
        rows.append(
            [log_type, param, uuid, ip, time, create_at, put_button('查看详情', onclick=partial(show_detail, log))])
    with use_scope('bag_items', clear=True):
        put_text("查询结果：")
        put_table(rows, header=['log_type', 'param', 'uuid', 'ip', 'time', 'create_at', 'detail'])
