from pywebio.output import put_text, put_table, use_scope
from pywebio_battery import get_localstorage

import mongodb_utils
from common import web_utils


def statis():
    app_db = web_utils.get_app_db_by_localstorage()
    count = mongodb_utils.get_uuid_count(app_db, "action_log")
    put_text(f"用户总数量：{count}")
    today_user_count = mongodb_utils.get_today_user_count(app_db, "action_log")
    put_text(f"今日活跃用户数量：{today_user_count}")
    # 每种类型的日志数量
    put_text("日志类型统计：")
    log_types = mongodb_utils.get_log_types(app_db, "action_log")
    log_type_counts = []
    for log_type in log_types:
        count = mongodb_utils.get_count(app_db, "action_log", {"log_type": log_type})
        log_type_counts.append([log_type, count])
    with use_scope('statis_table', clear=True):
        put_table(log_type_counts, header=['log_type', 'count'])

