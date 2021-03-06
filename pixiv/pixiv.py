from pixiv.spider import *
from pixiv.printer import *
import requests


def robust(actual_do): #用于防止闪退的try装饰器
    def add_robust(*args, **keyargs):
        try:
            return actual_do(*args, **keyargs)
        except:
            printer('Error execute: %s,已终止任务' % actual_do.__name__,'red')

    return add_robust



def isscalar(str):  # 判断输入是否均为数字，防止使用者将画师id与画师名称混淆
    try:
        float(str)
    except ValueError:
        printer('请输入正确的画师id(而非名字)', 'red', 1)
        exit()
        return False
    else:
        return True


def proxy_connect():  # 检查代理是否连接成功
    try:
        requests.get('http://google.com', timeout=5)
        printer('国际互联网响应成功，代理正常', 'green', 1)
    except:
        printer('国际互联网未响应，请检查代理设置', 'red', 1)
        exit()


@robust
def pix_id(id, limits=150, like=20, path='', single_dir=False, thread=5):
    '''
    画师搜索主函数封装
    :param id: 作者id
    :param limits: 最多获取数量
    :param like:最少喜欢
    '''
    isscalar(id)
    proxy_connect()
    lists = painter_spider(id, limits)
    download_all(lists, like, 0, path, single_dir, thread)


@robust
def pix_search(search, limits=150, like=20, path='', single_dir=False, thread=5):
    if search == '':
        printer('请输入关键字', 'red', 1)
        exit()
    proxy_connect()
    lists = search_spider(search, limits)
    download_all(lists, like, 1, path, single_dir, thread)


@robust
def pix_rank(limits=200, like=20, path='', single_dir=False, thread=5):
    proxy_connect()
    lists = ranking_spider(limits)
    download_all(lists, like, 2, path, single_dir, thread)
