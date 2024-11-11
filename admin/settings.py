from pywebio import config
from pywebio.output import put_text
from pywebio.session import set_env

from admin.header import navbar


@config(title="设置")
def main():
    set_env(output_max_width='80%')
    navbar()
    put_text("设置！")

