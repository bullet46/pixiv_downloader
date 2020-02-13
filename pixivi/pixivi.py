import requests
import json
import os
import threading as td

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36",
    "Referer": "https://www.pixiv.net"
}

path = ''


def splitshows(str):
    '''用于打印分割线，类似于-------分割线--------'''
    print('\033[32m' + '-' * 25 + str + '-' * 25 + '\033[0m')


def parser(uid):
    '''
    解析器，获取画作相关信息
    :param uid: 目标uid
    :return:[图片名字，图片链接，图片点赞]
    '''
    try:
        url = "http://pixiv.net/ajax/illust/{uid}".format(uid=uid)
        r = requests.get(url, headers=headers, timeout=5)
        json_back = json.loads(r.text)
        img_url = json_back['body']['urls']['original']
        img_name = json_back['body']['illustTitle']
        like = json_back['body']['bookmarkCount']
        backs = [img_name, img_url, like]
    except:
        backs = None
    return backs


def downloader(url, path):
    '''
    下载器，用于下载指定url图片并进行保存
    :param url: 图片地址
    :param path: 图片保存位置
    :return: 状态值0为成功
    '''
    r = requests.get(url, headers=headers).content
    try:
        with open(path, 'wb+') as f:
            f.write(r)
        return 0
    except:
        return -1


def download(uid, path='', like=10):
    '''
    :param uid: 作品uid
    :param path: 目标位置
    :param like: 最少喜欢人数,默认为10
    :return: 0成功，-1下载失败，-2解析失败，-3跳过
    '''
    back = parser(uid)
    if back is not None:
        if back[2] < like:
            print('\032{}:跳过\033[0m'.format(back[0]))
            return -3
        else:
            downsuccess = downloader(back[1], path + '/' + back[0] + '.jpg')
            print('\033[32m{}:下载成功\033[0m'.format(back[0]))
            if downsuccess != 0:
                print('\033[31m{}:下载失败 \033[0m'.format(back[0]))
                return -1
    else:
        print('\033[31m{}:解析失败 \033[0m'.format(uid))
        return -2


def painter_spider(id):
    '''
    用于爬取作者所有画作uid的爬虫
    :param id: 作家id
    :return:list:表示爬取到的画作列表,list[0]表示画家名称，之后代表画作id
    '''
    splitshows('开始爬取id：{}'.format(id))
    page = 1
    lists = []
    while True:
        url = 'https://www.pixiv.net/touch/ajax/user/illusts?id={id}&p={page}'.format(id=id, page=page)
        print('get:' + url)
        try:
            r = json.loads(requests.get(url).text)
            illusts_lists = r['body']['illusts']
            sum_number = len(illusts_lists)
            if page == 1:  # 在第一页获取作家姓名
                name = illusts_lists[0]['author_details']['user_name']
                lists.append(name)
            if sum_number == 0:  # 如果当页内作品数为0，可判定为最终页之后，表明已获取全部信息
                break
            for i in range(sum_number):
                lists.append(illusts_lists[i]['id'])
            print('success: 作家:{name}  第{page}页信息获取成功，已获取画作{number}'.format(name=name, page=page, number=len(lists) - 1))
            page += 1
        except:
            print('fail : 作家:{name}第{page}页信息获取失败'.format(name=name, page=page))
    splitshows('结束爬取id：{}'.format(id))
    return lists


def download_all(lists, limits=150, like=0, threads=3):
    '''
    线程创建与下载
    :param lists: 爬虫爬取得到的列表
    :param limits: 限制下载数量，默认为150
    :param like : 筛选最少喜欢人数:默认为0
    :param threads:线程数，默认为3
    :return: d_lists : 返还下载信息列表[[名字，链接],..]
    '''
    last_id = min(len(lists) - 1, limits)
    splitshows('开始下载画师:{}'.format(lists[0]))
    root_path = '# 画师_{name}  总数_{number}'.format(name=lists[0], number=last_id)
    if bool(1 - os.path.exists(root_path)):  # 判断是否存在画师目录，如果不存在，创建目录
        os.makedirs(root_path)

    for i in lists[1:]:
        try:
            locals()['t{}'.format(i)] = td.Thread(target=download, args=(i, root_path, like))
            print('\033[32m 成功创建线程:{} \033[0m'.format(i))
            locals()['t{}'.format(i)].start()
        except:
            print("Error: 无法启动线程")
    print(splitshows('创建完成'))


def pix(id, limits=150, like=20):
    '''
    主函数封装
    :param id: 作者id
    :param limits: 最多获取数量
    :param like:最少喜欢
    '''
    lists = painter_spider(id)
    download_all(lists, limits, like)
