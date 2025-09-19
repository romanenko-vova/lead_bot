import time

def foo1():
    time.sleep(3)
    print(1)
    # for i in range(200000000):
    #     i = i + i
    # print(i)

def foo2():
    time.sleep(5)
    print(2)


def foo3():
    time.sleep(2)
    print(3)

ts = time.time()
foo1()
foo2()
foo3()
print(time.time() - ts)
