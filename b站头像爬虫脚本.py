import requests
import json
import threading as td
import time


def input_uid():
    uid_between = [0, 0]
    uid_between[0] = int(input('初始uid:'))
    uid_between[1] = int(input('结束uid:'))
    return uid_between


def downloader(uid):
    url = 'https://api.bilibili.com/x/space/acc/info?mid=' + str(uid) + '&jsonp=jsonp'
    try:
        r = requests.get(url)
        dic = json.loads(r.text)
        img_name = dic['data']['name']  # 取得名字
        img_url = dic['data']['face']  # 取得图片位置
        img = requests.get(img_url, timeout=3)
        excepts = ['http://static.hdslb.com/images/member/noface.gif', 'http://i2.hdslb.com/bfs/face/5d2c92beb774a4bb30762538bb102d23670ae9c0.gif', 'http://i1.hdslb.com/bfs/face/5d2c92beb774a4bb30762538bb102d23670ae9c0.gif']
        for strs in excepts:
            if img_url == strs:
                return -2

        with open(str('uid' + str(uid) + '-' + img_name + '.jpg'), "wb") as f:
            f.write(img.content)
            print('----{}_{}下载成功----'.format(uid, img_name))
            return 0

    except:
        print('****' + str(uid) + ':下载失败****')
        return -1


def download(between, speed):
    for i in range(between[0], between[1] + 1):
        try:
            locals()['t{}'.format(i)] = td.Thread(target=downloader, args=(i,))
            print('## 正在下载:{}  ##'.format(i))
            locals()['t{}'.format(i)].start()
        except:
            print("Error: 无法启动线程")
        time.sleep(speed)


def main():
    lists = input_uid()
    speed = int(input('请设置速度，越大越快(例如1为1张/秒,最多为10):'))
    if speed >= 10 or speed <= 0:
        speed = 10
    speed = 1 / speed
    download(lists, speed)


if __name__ == '__main__':
    main()
