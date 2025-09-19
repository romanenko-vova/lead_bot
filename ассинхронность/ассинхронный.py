import time
import asyncio

# coroutine - ассинхронная функция
async def foo1():
    print('1.1')
    await asyncio.sleep(3)
    for i in range(200000000):
        i = i + i
    print(i)
    print('1.2')
    

async def foo2():
    print('2.1')
    await asyncio.sleep(5)
    print('2.2')


async def foo3():
    print('3.1')
    await asyncio.sleep(2)
    print('3.2')

async def main():
    task1 = asyncio.create_task(foo1())
    task2 = asyncio.create_task(foo2())
    task3 = asyncio.create_task(foo3())
    await task1
    await task2
    await task3

ts = time.time()
asyncio.run(main())
print(time.time() - ts)
