import datetime
import logging
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, Request

from logger_utils import init_logging_basic_config
from mongodb_utils import add_log

app = FastAPI()


@app.post("/log")
async def log_function(data: Dict[str, Any]):
    # 检查是否有 'type' 键
    if 'log_type' not in data:
        return {"message": "JSON data must contain 'log_type' field."}
    logging.info(f"The 'log_type' value is: {data['log_type']}")
    add_log(data)
    return {"message": "Logged successfully"}


@app.get("/hello")
async def hello_world():
    return {"message": "Hello, world!"}


@app.get("/get_ip")
async def get_ip(request: Request):
    ip = request.client.host
    logging.info(f"ip={ip}")
    return {"ip": ip}


if __name__ == "__main__":
    init_logging_basic_config()
    uvicorn.run(app, host="0.0.0.0", port=8014)
