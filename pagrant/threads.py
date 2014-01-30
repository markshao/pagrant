#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from threading import Thread


def thread_map(iter, target, **kwargs):
    # the different map implementation base on thread
    # def target(item,name):
    #     pass
    # iter = [item1,item2]
    # thread_map(iter,target,**(dict(name="a"))

    thread_list = []

    for item in iter:
        thread = Thread(target=target, args=[item], kwargs=kwargs)
        thread.daemon = True
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == "__main__":
    def test(item, bench):
        print "%s%s" % (item, bench)

    thread_map(["mark", "archer"], test, **dict(bench="bbb"))