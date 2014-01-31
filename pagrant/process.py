#!/usr/bin/python
#coding:utf8

__author__ = ['markshao']

from multiprocessing import Process


def process_map(iter, target, **kwargs):
    # the different map implementation base on thread
    # def target(item,name):
    #     pass
    # iter = [item1,item2]
    # process_map(iter,target,**(dict(name="a"))

    process_list = []

    for item in iter:
        process = Process(target=target, args=[item], kwargs=kwargs)
        process.daemon = True
        process_list.append(process)
        process.start()

    for process in process_list:
        process.join()


if __name__ == "__main__":
    def test(item, bench):
        print "%s%s" % (item, bench)

    process_map(["mark", "archer"], test, **dict(bench="bbb"))