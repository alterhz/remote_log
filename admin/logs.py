import copy
import datetime
import logging
from functools import partial

from pywebio import config
from pywebio.output import put_text, use_scope, put_table, put_button, popup
from pywebio.session import set_env

from admin.header import navbar
from mongodb_utils import search_last_logs


@config(title="日志")
def main():
    set_env(output_max_width='80%')
    navbar()
    put_text("查询结果")
    get_all_logs()


def show_detail(log):
    popup(f"日志详情: {log['log_type']}", [
        put_text(f"{log}"),
    ])


def get_all_logs():
    logs = search_last_logs({}, 100)
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
        put_table(rows, header=['log_type', 'param', 'uuid', 'ip', 'time', 'create_at', 'detail'])
