import logging
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, Request

import mongodb_utils
from logger_utils import init_logging_basic_config

app = FastAPI()


@app.post("/log")
async def log_function(data: Dict[str, Any]):
    # 检查是否有 'type' 键
    if 'log_type' not in data:
        return {"message": "JSON data must contain 'log_type' field."}
    logging.info(f"The 'log_type' value is: {data['log_type']}")
    mongodb_utils.append_log("excel_sheet_master", "action_log", data)
    return {"message": "Logged successfully"}


@app.post("/merge_editor_log")
async def merge_editor_log(data: Dict[str, Any]):
    # 检查是否有 'type' 键
    if 'log_type' not in data:
        return {"message": "JSON data must contain 'log_type' field."}
    logging.info(f"The 'log_type' value is: {data['log_type']}")
    last_append_id = mongodb_utils.append_log("merge_editor", "action_log", data)
    return {"message": "Logged successfully. Last append id: " + str(last_append_id)}


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
