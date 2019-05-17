from datetime import datetime
from py.xml import html
import pytest

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    #cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.insert(3, html.th('Params'))
    cells.insert(2, html.th('Description'))
    cells.insert(0, html.th('No.'))
    cells.pop()

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    #cells.insert(1, html.td(datetime.utcnow(), class_='col-time'))
    cells.insert(3, html.td(report.params))
    cells.insert(2, html.td(report.description))
    cells.insert(0, html.td(report.number))
    cells.pop()

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # 对test一列重新编码，显示中文
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")
    # test列中包含了测试用例传入的所以参数，先对其进行分割
    result = report.nodeid.split('-')
    # 从test列剥离出不同的参数信息
    number = result[0].split('[')[1]
    api_name = result[1]
    description = result[2]
    url = result[4]
    request_method = result[5]
    params = result[6]
    check_point = result[8]
    # 对新插入的表格进行赋予参数值
    report.nodeid = api_name + ' -- ' + request_method + ' -- ' + url
    report.description = str(description)
    report.number = str(number)
    report.url = str(url)
    report.params = str(params)

