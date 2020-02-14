import requests
import json
import os
import threading as td

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36",
    "Referer": "https://www.pixiv.net"
}  # 请求头

save_path = ''  # 保存路径，默认为当前路径
timeout = 200  # 最大等待时间，若网速过慢导致连接超时，可适当调大


def splitshows(str):
    '''用于打印分割线，类似于-------分割线--------'''
    print('\033[32m' + '-' * 25 + str + '-' * 25 + '\033[0m')


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
        print(img_name + ':解析超时')
        backs = None
    except:
        print(str(uid) + ':解析失败')
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
        print('\033[33m正在下载:{path}\033[0m'.format(path=path))
        with open(path, 'wb+') as f:
            f.write(r)
        return 0
    except TimeoutError:
        print(path + ':下载超时')
    except:
        print(path + ':下载失败')


def downloader(uid, path='', like=0):
    '''
    下载器
    :param uid: 作品uid
    :param path: 目标位置
    :param like: 最少喜欢人数,默认为0
    :return: 0成功，-1下载失败，-2解析失败，-3跳过
    '''
    back = parser(uid)
    if back is not None:
        if back[2] < like:
            print('\032{}:跳过\033[0m'.format(back[0]))
            return -3
        else:
            for i in range(len(back[1])):
                if i == 0:
                    downsuccess = reservoir(back[1][i], '{path}{name}.jpg'.format(path=path, name=back[0]))
                else:
                    downsuccess = reservoir(back[1][i], '{path}{name}_p{i}.jpg'.format(path=path, name=back[0], i=i))
                if downsuccess == 0:
                    print('\033[32m{}p{}:下载成功\033[0m'.format(back[0], i))
    else:
        return -2


def painter_spider(id, limits=200):
    '''
    用于爬取画师所有画作uid的爬虫
    :param id: 作家id
    :param limits:限制器，默认200画作
    :return:list:表示爬取到的画作列表,list[0]表示画家名称，之后代表画作id
    '''
    splitshows('开始爬取id：{}'.format(id))
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
            print('success: 画师:{name}  第{page}页信息获取成功，已获取画作{number}'.format(name=name, page=page, number=min(all_arts, limits)))
            page += 1
        except:
            print('fail : 画师:{name}第{page}页信息获取失败'.format(name=name, page=page))
    splitshows('结束爬取id：{}'.format(id))
    return lists[:min(limits, all_arts) + 1]


def download_all(lists, like=0):
    '''
    线程创建与下载
    :param lists: 爬虫爬取得到的列表
    :param limits: 限制下载数量，默认为150
    :param like : 筛选最少喜欢人数:默认为0
    :return: d_lists : 返还下载信息列表[[名字，链接],..]
    '''
    last_id = len(lists) - 1
    splitshows('开始下载画师:{}'.format(lists[0]))
    root_path = save_path + '# 画师_{name}  画册总数_{number}\\'.format(name=lists[0], number=last_id)
    if bool(1 - os.path.exists(root_path)):  # 判断是否存在画师目录，如果不存在，创建目录
        os.makedirs(root_path)

    for i in lists[1:]:
        try:
            locals()['t{}'.format(i)] = td.Thread(target=downloader, args=(i, root_path, like))
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
    lists = painter_spider(id,limits)
    download_all(lists, like)


if __name__ == '__main__':
    lists = painter_spider(418969)
    download_all(lists)
