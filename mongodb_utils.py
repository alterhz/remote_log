import logging
from datetime import datetime, timedelta

import pymongo

client = pymongo.MongoClient("mongodb://10.4.4.123:27017/")
print(f"Connected to MongoDB!{client}")


def append_log(db, collection_name, json_log):
    """
    添加日志
    :param db: 数据库名称
    :param collection_name: 集合名称
    :param json_log: 日志内容
    :return: None
    """
    logging.info(f"add log: {json_log}")
    # 追加当前时间戳long
    json_log['create_at'] = datetime.now().timestamp()
    mydb = client[db]
    action_log = mydb[collection_name]
    one = action_log.insert_one(json_log)
    logging.info(f"Inserted log with id: {one.inserted_id}")
    return one.inserted_id


def search_last_logs(db, collection_name, json_data, limit=10):
    """
    查询最新10条记录
    :param json_data:
    :return:
    """
    mydb = client[db]
    action_log = mydb[collection_name]
    # 查询所有日志，以便返回
    logs = action_log.find(json_data).sort("create_at", pymongo.DESCENDING).limit(limit)
    return logs


def get_uuid_count(db, collection_name):
    mydb = client[db]
    action_log = mydb[collection_name]
    uuids = action_log.distinct("uuid")
    return len(uuids)


def get_today_user_count(db, collection_name):
    mydb = client[db]
    action_log = mydb[collection_name]

    # 获取今天的日期（起始时间和结束时间）
    today_start = datetime.combine(datetime.today(), datetime.min.time())
    today_end = datetime.combine(datetime.today(), datetime.max.time())

    # 查询今天内有操作记录的不同uuid数量，即今天的用户量
    uuids = action_log.distinct("uuid",
                                {"create_at": {"$gte": today_start.timestamp(), "$lte": today_end.timestamp()}})

    return len(uuids)


def get_week_user_count(db, collection_name):
    """
    获取本周的用户量
    :param db:   数据库名称
    :param collection_name: 集合名称
    :return: 本周的用户量
    """
    mydb = client[db]
    action_log = mydb[collection_name]
    # 获取本周的起始时间和结束时间
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    # 查询本周内有操作记录的不同uuid数量，即本周的用户量
    uuids = action_log.distinct("uuid",
                                {"create_at": {"$gte": start_of_week.timestamp(), "$lte": end_of_week.timestamp()}})
    return len(uuids)


def get_month_user_count(db, collection_name):
    """
    获取本月用户量
    :param db: 数据库名称
    :param collection_name: 集合名称
    :return: 本月用户量
    """
    mydb = client[db]
    action_log = mydb[collection_name]
    # 获取本月的起始时间和结束时间
    today = datetime.today()
    # 考虑跨年的情况
    if today.month == 1:
        last_month_start = datetime(today.year - 1, 12, 1)
    else:
        last_month_start = datetime(today.year, today.month - 1, 1)

    last_month_end = datetime(today.year, today.month, 1) - timedelta(seconds=1)
    # 查询本月内有操作记录的不同uuid数量，即本月的用户量
    uuids = action_log.distinct("uuid",
                                {"create_at": {"$gte": last_month_start.timestamp(), "$lte": last_month_end.timestamp()}})
    return len(uuids)


def get_day_user_count(db, collection_name, date):
    """
    获取指定日期的用户量
    :param db: 数据库名称
    :param collection_name: 集合名称
    :param date: 日期
    :return: 指定日期的用户量
    """
    mydb = client[db]
    action_log = mydb[collection_name]
    # 获取指定日期的起始时间和结束时间
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())
    # 查询指定日期内有操作记录的不同uuid数量，即指定日期的用户量
    uuids = action_log.distinct("uuid",
                                {"create_at": {"$gte": start_of_day.timestamp(), "$lte": end_of_day.timestamp()}})
    return len(uuids)



def get_log_types(db, collection_name):
    mydb = client[db]
    action_log = mydb[collection_name]
    action_types = action_log.distinct("log_type")
    return action_types


def get_count(db, collection_name, json_filter):
    mydb = client[db]
    action_log = mydb[collection_name]
    count = action_log.count_documents(json_filter)
    return count


def clear_logs():
    mydb = client["excel_sheet_master"]
    action_log = mydb["action_log"]
    action_log.delete_many({})
    logging.info("All logs have been cleared.")


if __name__ == '__main__':
    print("all logs:")
    logs = search_last_logs({})
    for log in logs:
        print(log)
