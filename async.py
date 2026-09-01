import asyncio
import time

async def work():
    print("start")
    await asyncio.sleep(1)
    print("end")