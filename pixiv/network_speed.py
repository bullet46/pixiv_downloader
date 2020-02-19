'''
网络测速模块
'''
import psutil
import time


def speed_test():
    time.clock()
    net_io = psutil.net_io_counters(pernic=True)
    s1, s2 = 0, 0
    for key in net_io.keys():
        s1 += net_io[key].bytes_recv
    time.sleep(1)
    net_io = psutil.net_io_counters(pernic=True)
    for key in net_io.keys():
        s2 += net_io[key].bytes_recv
    result = s2 - s1
    # 除法结果保留两位小数
    return str('%.2f' % (result / 1024)) + 'kb/s'

if __name__ =='__main__':
    while True:
        print(speed_test())
