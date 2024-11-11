import pymongo

client = pymongo.MongoClient("mongodb://10.4.4.123:27017/")
print(f"Connected to MongoDB!{client}")


def add_log(json_log):
    print(f"{json_log}")
    mydb = client["excel_sheet_master"]
    action_log = mydb["action_log"]
    one = action_log.insert_one(json_log)
    print(f"Inserted log with id: {one.inserted_id}")


def search_log(json_data):
    mydb = client["excel_sheet_master"]
    action_log = mydb["action_log"]
    # 查询所有日志，以便返回
    logs = action_log.find(json_data)
    return logs


if __name__ == '__main__':
    print("all logs:")
    logs = search_log({})
    for log in logs:
        print(log)
