from test1 import f
def f2():
    print(2, __name__)
    f()
    
f2()