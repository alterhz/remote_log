import datetime
from functools import partial

from pywebio import config
from pywebio.output import put_text, use_scope, put_table, put_button, popup
from pywebio.session import set_env

from admin.header import navbar
from mongodb_utils import search_log, search_last_logs


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
        # log['uuid']不存在返回""
        uuid = ""
        if log.get('uuid'):
            uuid = log['uuid']
        time = ""
        if log.get('time'):
            time = log['time']
        timestamp = ""
        if log.get('timestamp'):
            timestamp = log['timestamp']
            # try:
            #     dt = datetime.datetime.fromtimestamp(timestamp)
            #     timestamp = dt.strftime('%Y-%m-%d %H:%M:%S.%f')
            # except Exception as e:
            #     pass

        ip = ""
        if log.get('ip'):
            ip = log['ip']
        param = ""
        log_type = log['log_type']
        if log_type == 'search':
            param = f"search_type_index: {log['search_type_index']}, search_text: {log['search_text']}"
        elif log_type == 'change_dir':
            param = f"path: {log['path']}"
        elif log_type == 'add_new_path':
            param = f"new_path: {log['new_path']}"
        elif log_type == 'open_excel':
            param = f"excel_name: {log['excel_name']}, sheet_name: {log['sheet_name']}"

        # 按钮弹窗显示log
        rows.append([log_type, param, uuid, ip, time, timestamp, put_button('查看详情', onclick=partial(show_detail, log))])
    with use_scope('bag_items', clear=True):
        put_table(rows, header=['log_type', 'param', 'uuid', 'ip', 'time', 'timestamp', 'detail'])
