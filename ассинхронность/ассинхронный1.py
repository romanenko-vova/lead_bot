import time
import asyncio

# coroutine - ассинхронная функция
async def foo1():
    await asyncio.sleep(3)
    print('1')

async def foo2():
    await asyncio.sleep(5)
    print('2')

async def foo3():
    await asyncio.sleep(2)
    print('3')

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
