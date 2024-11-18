from pywebio_battery import get_localstorage

import mongodb_utils


def get_app_db_by_localstorage():
    app_name = get_localstorage('app_name')
    if app_name == '页签搜索大师':
        return 'excel_sheet_master'
    elif app_name == 'Excel合并工具':
        return 'excel_merge'
    else:
        return 'unknown'
