import datetime
import logging

import pymongo
from pywebio.output import use_scope, put_table

client = pymongo.MongoClient("mongodb://10.4.4.123:27017/")
print(f"Connected to MongoDB!{client}")


def add_log(json_log):
    logging.info(f"add log: {json_log}")
    # 追加当前时间戳long
    json_log['create_at'] = datetime.datetime.now().timestamp()
    mydb = client["excel_sheet_master"]
    action_log = mydb["action_log"]
    one = action_log.insert_one(json_log)
    logging.info(f"Inserted log with id: {one.inserted_id}")


def search_last_logs(json_data, limit=10):
    """
    查询最新10条记录
    :param json_data:
    :return:
    """
    mydb = client["excel_sheet_master"]
    action_log = mydb["action_log"]
    # 查询所有日志，以便返回
    logs = action_log.find(json_data).sort("create_at", pymongo.DESCENDING).limit(limit)
    return logs


def clear_logs():
    mydb = client["excel_sheet_master"]
    action_log = mydb["action_log"]
    action_log.delete_many({})


if __name__ == '__main__':
    print("all logs:")
    logs = search_last_logs({})
    for log in logs:
        print(log)
