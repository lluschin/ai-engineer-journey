import asyncio
import random as rnd



async def fetch_data(id: int, delay: float) -> dict:
    print("start fetching data..")
    
    await asyncio.sleep(delay)
    data = {"id" : id,
            "data" : str(rnd.randint(100, 999))}

    print(f"id::{id} data is fetched")

    return data


async def first_job(): # running with async but still linear!
    print("running first job")
    task1 = fetch_data(1, 2)
    task2 = fetch_data(2, 2)

    result1 = await task1
    print(f"data: {result1}")

    result2 = await task2
    print(f"data: {result2}")


async def second_job(): # running tasks in paralell
    print("running second job")
    task1 = asyncio.create_task(fetch_data(1, 2.4))
    task2 = asyncio.create_task(fetch_data(2, 2.7))
    task3 = asyncio.create_task(fetch_data(3, 2.1))

    result1 = await task1
    # print(result1) <-- would execute task1 and waits.. than continues
    result2 = await task2
    result3 = await task3

    print(result1)
    print(result2)
    print(result3)


async def third_job(): # running tasks in paralell and gather
    print("running third job")
    results = await asyncio.gather(fetch_data(1, 2.4),
                                   fetch_data(2, 2.7),
                                   fetch_data(3, 2.1))

    for result in results:
        print(result)



if __name__ == "__main__":
    asyncio.run(third_job())