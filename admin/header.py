from pywebio.output import put_link, put_grid


def navbar():
    grid_items = [put_link("首页", url="/"), put_link("日志", url="/logs"), put_link("设置", url="/settings")]
    put_grid([
        grid_items
    ]).style('background-color: #e9ecef; margin: 10px; font-size: 1.5em; text-align: center; border-radius: 5px;')
