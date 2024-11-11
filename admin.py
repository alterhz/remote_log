
from pywebio import config
from pywebio.platform import path_deploy_http

from logger_utils import init_logging_basic_config

config(theme="yeti")

if __name__ == '__main__':
    # confs.load_data()
    init_logging_basic_config()
    path_deploy_http("admin/", port=8015, static_dir="static")
