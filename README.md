# remote_log
远端日志，用于记录app的操作行为


# 启动fastapi
```shell
# 控制台启动
python main.py
```

# 启动后台
```shell

```


# docker 安装mongodb
```shell
# 拉取镜像
docker pull mongo
# 运行mongo
docker run -d -p 27017:27017 --name my-mongo mongo
# 停止
docker stop my-mongo
```

# docker 持久化安装mongodb
```shell
# 数据持久化
docker volume create mongo-data
# 查看volume
docker volume ls
# 运行mongo
docker run -d -p 27017:27017 --name my-mongo -v mongo-data:/data/db mongo
```
