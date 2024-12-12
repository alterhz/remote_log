import logging
from datetime import datetime, timedelta

from pywebio.output import put_text, put_table, use_scope
from pywebio_battery import get_localstorage

import mongodb_utils
from common import web_utils


def recent_user_count():
    app_db = web_utils.get_app_db_by_localstorage()
    # 获取今天的date，然后循环近30天
    header = []
    user_count = []
    today = datetime.today()
    for i in range(30):
        date = today - timedelta(days=i)
        month_user_count = mongodb_utils.get_day_user_count(app_db, "action_log", date)
        logging.info(f"{date.strftime('%Y-%m-%d')}：{month_user_count}")
        header.append(date.strftime('%m-%d'))
        user_count.append(month_user_count)

    with use_scope('recent_user_count', clear=True):
        put_text(f'最近30天活跃用户数量：')
        put_table([header, user_count])





def statis():
    app_db = web_utils.get_app_db_by_localstorage()
    count = mongodb_utils.get_uuid_count(app_db, "action_log")
    put_text(f"用户总数量：{count}")
    today_user_count = mongodb_utils.get_today_user_count(app_db, "action_log")
    put_text(f"今日活跃用户数量：{today_user_count}")
    week_user_count = mongodb_utils.get_week_user_count(app_db, "action_log")
    put_text(f"本周活跃用户数量：{week_user_count}")
    month_user_count = mongodb_utils.get_month_user_count(app_db, "action_log")
    put_text(f"本月活跃用户数量：{month_user_count}")

    recent_user_count()

    # 每种类型的日志数量
    put_text("日志类型统计：")
    log_types = mongodb_utils.get_log_types(app_db, "action_log")
    log_type_counts = []
    for log_type in log_types:
        count = mongodb_utils.get_count(app_db, "action_log", {"log_type": log_type})
        log_type_counts.append([log_type, count])
    with use_scope('statis_table', clear=True):
        put_table(log_type_counts, header=['log_type', 'count'])

