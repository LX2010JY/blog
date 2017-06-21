#coding:utf8
import time
'''
公共函数
'''
def timestamp():
    '''
    获取当前时间戳
    :return:
    '''
    tamp = time.time()
    return int(tamp)

def str_to_timestamp(tstr):
    '''
    字符串转时间戳
    :param tstr: 符合格式的时间字符串
    :return: 时间戳
    '''
    #转成时间数组
    timeArray = time.strptime(tstr,"%Y-%m-%d %H:%M:%S")
    #转为时间戳
    timestamp = time.mktime(timeArray)
    return int(timestamp)

def timestamp_to_str(tamp):
    '''
    时间戳转回字符串时间
    :param tamp:  时间戳
    :return:
    '''
    #时间戳转回时间数组 与 mktime作用相反
    time_local = time.localtime(tamp)
    tstr = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    return tstr