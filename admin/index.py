from functools import partial

from pywebio import config
from pywebio.output import put_text, put_row, put_button, toast
from pywebio.pin import put_select, pin
from pywebio.session import set_env
from pywebio_battery import get_localstorage, set_localstorage

from admin.header import navbar
from admin.statis import statis


@config(title="首页")
def main():
    set_env(output_max_width='80%')
    navbar()
    put_text("欢迎使用行为日志管理后台！")
    put_row([
        put_text('选择app：').style('font-size:20px; margin-left: 10px; margin-top:5px; text-align:right; '),
        put_select('app_name', options=['页签搜索大师', 'Excel合并工具'],
                   value=get_localstorage('app_name')),
        put_button('切换app', onclick=partial(switch_app)).style('margin-left:5px; ')
    ], size="120px 200px 100px")

    statis()


def switch_app():
    set_localstorage('app_name', pin.app_name)
    toast(f'已切换到{pin.app_name}')
