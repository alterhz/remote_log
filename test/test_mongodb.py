import pymongo

# 创建MongoClient对象，连接本地MongoDB服务器，默认端口是27017
client = pymongo.MongoClient("mongodb://10.4.4.123:27017/")
print(client)

mydb = client["mydatabase"]
mycol = mydb["mycollection"]

data = {"name": "John2", "age": 30}
x = mycol.insert_one(data)
print(x.inserted_id)

data_list = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 35}]
x = mycol.insert_many(data_list)
print(x.inserted_ids)

for x in mycol.find():
    print(x)


query = {"name": "John"}
new_values = {"$set": {"age": 31}}
mycol.update_one(query, new_values)


query = {"name": "Alice"}
mycol.delete_one(query)

query = {"age": {"lt": 30}}
mycol.delete_many(query)

print("final:")
for x in mycol.find():
    print(x)