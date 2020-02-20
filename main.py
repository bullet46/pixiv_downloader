from pixiv.pixiv import *
from pixiv.spider import *

# pix_id(4819066, limits=100, like=10)

# pix_search('初音未来',limits=200,like=0 )
def main():
    pix_search('初音未来', limits=200, like=0)

'''
运行前请确认是否成功连接代理
作者id爬虫：pix_id(作者id,最多获取数，最少喜爱)
搜索结果爬虫：pix_search(搜索内容，最多获取数，最少喜爱)
排名爬虫：pix_rank(最多获取数，最少喜爱)
'''
