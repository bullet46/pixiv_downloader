import requests
import json
import os
import sys
import threading as td
import datetime
# from pixiv.printer import *
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36",
    "Referer": "https://www.pixiv.net"
}  # 请求头，请勿更改

timeout = 200  # 最大等待时间，若网速过慢导致连接超时，可适当调大


def parser(uid):
    '''
    解析器，获取画作相关信息
    :param uid: 目标uid
    :return:[图片名字，[图片链接1,图片链接2,..]，图片点赞] ps:可能存在画册,具有多个链接
    '''
    img_urls = []
    try:
        info_url = "http://pixiv.net/ajax/illust/{uid}".format(uid=uid)
        download_url = "http://pixiv.net/ajax/illust/{uid}/pages".format(uid=uid)
        r = requests.get(info_url, timeout=timeout)
        r_d = requests.get(download_url, timeout=timeout)
        json_info = json.loads(r.text)
        json_down = json.loads(r_d.text)
        for i in range(len(json_down['body'])):
            img_urls.append(json_down['body'][i]['urls']['original'])
        img_name = json_info['body']['illustTitle']
        like = json_info['body']['bookmarkCount']
        backs = [img_name, img_urls, like]
    except TimeoutError:
        printer(img_name + ':解析超时', 'red')
        backs = None
    except:
        printer(str(uid) + ':解析失败', 'red')
        backs = None
    return backs


def reservoir(url, path):
    '''
    储存器，用于下载指定url图片并进行保存
    :param url: 图片地址
    :param path: 图片保存位置
    :return: 状态值0为成功
    '''
    try:
        r = requests.get(url, headers=headers, timeout=timeout).content
        printer('正在下载:{path}'.format(path=path), 'yellow')
        if os.path.exists(path):
            printer('已存在文件:{}'.format(path), 'green')
            return 0
        with open(path, 'wb+') as f:
            f.write(r)
        printer(path + '下载成功', 'green')
        return 0
    except TimeoutError:
        printer(path + ':下载超时', 'red')
    except:
        printer(path + ':下载失败', 'red')


def downloader(uid, path='', like=0, single_dir=False):
    '''
    下载器
    :param uid: 作品uid
    :param path: 目标位置
    :param like: 最少喜欢人数,默认为0
    :param single_dir:将画册分离至单独文件夹
    :return: 0成功，-1下载失败，-2解析失败，-3跳过
    '''
    back = parser(uid)
    if back is not None:
        if back[2] < like:
            printer('{}:跳过,不符合喜爱限制'.format(back[0]), 'green')
            return -3
        else:
            number = len(back[1])
            if single_dir and number != 1:
                if bool(1 - os.path.exists(path + '画册子_{}'.format(back[0]))):  # 判断是否存在画册目录，如果不存在，创建目录
                    os.makedirs(path + '画册_{}'.format(back[0]))
                path = path + '画册_{}\\'.format(back[0])
                print(path)
            for i in range(number):
                if i == 0:
                    reservoir(back[1][i], '{path}{name}.jpg'.format(path=path, name=back[0]))
                else:
                    reservoir(back[1][i], '{path}{name}_p{i}.jpg'.format(path=path, name=back[0], i=i))

    else:
        return -2


def painter_spider(id, limits=200):
    '''
    用于爬取画师所有画作uid的爬虫
    :param id: 作家id
    :param limits:限制器，默认200画作
    :return:list:表示爬取到的画作列表,list[0]表示画家名称，之后代表画作id
    '''
    printer('开始爬取id：{}'.format(id), 'yellow', 1)
    page = 1
    all_arts = 0
    lists = []
    while all_arts <= limits:  # 如果目前所获得的的作品少于限定,则跳出循环
        url = 'https://www.pixiv.net/touch/ajax/user/illusts?id={id}&p={page}'.format(id=id, page=page)
        print('get:' + url)
        try:
            r = json.loads(requests.get(url).text)
            illusts_lists = r['body']['illusts']
            sum_number = len(illusts_lists)
            all_arts += sum_number
            if page == 1:  # 在第一页获取作家姓名
                name = illusts_lists[0]['author_details']['user_name']
                lists.append(name)
            if sum_number == 0:  # 如果当页内作品数为0，可判定为最终页之后，表明已获取全部信息
                break
            for i in range(sum_number):
                lists.append(illusts_lists[i]['id'])
            printer('success: 画师:{name}  第{page}页信息获取成功，已获取画作{number}'.format(name=name, page=page, number=min(all_arts, limits)), 'green')
            page += 1
        except:
            printer('fail : 画师:{name}第{page}页信息获取失败'.format(name=name, page=page), 'red')
    printer('结束爬取id：{}'.format(id), 'yellow', 1)
    return lists[:min(limits, all_arts) + 1]


def search_spider(search, limits=200):
    '''
    用于爬取搜索结果的爬虫
    :param search: 需要搜索的字符
    :param limits: 限制器，默认爬取200册
    :return: list:表示爬取到的画作列表,list[0]表示搜索名称，之后代表画作id
    '''
    printer('开始爬取搜索结果：{}'.format(search), 'yellow', 1)
    page = 1
    all_arts = 0
    lists = []
    while all_arts <= limits:  # 如果目前所获得的的作品少于限定,则跳出循环
        url = 'https://www.pixiv.net/ajax/search/artworks/{search}?p={page}'.format(search=search, page=page)
        print('get:' + url)
        try:
            r = json.loads(requests.get(url).text)
            illusts_lists = r['body']['illustManga']['data']
            sum_number = len(illusts_lists)
            lists.append(search)
            if sum_number == 0:  # 如果当页内作品数为0，可判定为最终页之后，表明已获取全部信息
                break
            for i in range(sum_number):
                try:
                    lists.append(illusts_lists[i]['id'])
                except KeyError:
                    sum_number -= 1
            all_arts += sum_number
            printer('success: 搜索结果:{name}  第{page}页信息获取成功，已获取画作{number}'.format(name=search, page=page, number=min(all_arts, limits)), 'green')
        except:
            printer('fail : 搜索结果:{name}第{page}页信息获取失败'.format(name=search, page=page), 'red')
        page += 1
    printer('结束爬取搜索：{}'.format(search), 'yellow', 1)
    return lists[:min(limits, all_arts) + 1]


def ranking_spider(limits=200):
    '''
    排名爬取器
    :param limits: 最少爬取数量
    :return: list：列表第一号元素返还时间，其余为所得作品id
    '''
    today = datetime.date.today()
    printer('开始爬取今日{}排行榜'.format(today), 'yellow', 1)
    page = 1
    all_arts = 0
    lists = []
    while all_arts <= limits:  # 如果目前所获得的的作品少于限定,则跳出循环
        url = 'https://www.pixiv.net/ranking.php?p={}&format=json'.format(page)
        print('get:' + url)
        try:
            r = json.loads(requests.get(url).text)
            illusts_lists = r['contents']
            sum_number = len(illusts_lists)
            lists.append(str(today))
            if sum_number == 0:  # 如果当页内作品数为0，可判定为最终页之后，表明已获取全部信息
                break
            for i in range(sum_number):
                try:
                    lists.append(illusts_lists[i]['illust_id'])
                except KeyError:
                    sum_number -= 1
            all_arts += sum_number
            printer('success: 今日排名:{name}  第{page}页信息获取成功，已获取画作{number}'.format(name=today, page=page, number=min(all_arts, limits)), 'green')
        except TimeoutError:
            printer('fail : 今日排名:{name}  第{page}页信息获取失败'.format(name=today, page=page), 'red')
        page += 1
    printer('结束爬取今日{}排行榜'.format(today), 'yellow', 1)
    return lists[:min(limits, all_arts) + 1]


def download_all(lists, like=0, mode=0, save_path='', single_dir=False, thread=5):
    '''
    线程创建与下载
    :param lists: 爬虫爬取得到的列表
    :param like : 筛选最少喜欢人数:默认为0
    :param mode : 爬取模式，如果为0代表爬取画师，1代表爬取搜素结果,2代表爬取排名
    :param save_path:根目录
    :param single_dir:是否将画册放入单独文件夹
    :param thread : 创建线程数
    '''
    last_id = len(lists) - 1
    if mode == 0:
        printer('开始下载画师:{}'.format(lists[0]), 'yellow', 1)
        root_path = save_path + '# 画师_{name}  画册总数_{number}\\'.format(name=lists[0], number=last_id)
    if mode == 1:
        printer('开始下载搜索结果:{}'.format(lists[0]), 'yellow', 1)
        root_path = save_path + '# 搜索内容_{name}  画册总数_{number}\\'.format(name=lists[0], number=last_id)
    if mode == 2:
        printer('开始下载今日排行:{}'.format(lists[0]), 'yellow', 1)
        root_path = save_path + '# 排行榜_{name}  画册总数_{number}\\'.format(name=lists[0], number=last_id)
    if bool(1 - os.path.exists(root_path)):  # 判断是否存在画册目录，如果不存在，创建目录
        os.makedirs(root_path)

    for i in lists[1:]:  # 对于每个特定任务
        while True:
            if (td.activeCount() - 1) <= thread:  # 如果总线程数小于既定线程，则可以添加新线程
                try:
                    locals()['t{}'.format(i)] = td.Thread(target=downloader, args=(i, root_path, like, single_dir))
                    printer('*成功载入线程:{}'.format(i), 'green')
                    locals()['t{}'.format(i)].start()
                    break
                except:
                    printer('error', 'red')
    printer('创建完成', 'yellow', 1)


