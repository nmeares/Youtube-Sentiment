import asyncio

class test():
    async def factorial(name, number):
        f = 1
        for i in range(2, number + 1):
            print(f"Task {name}: Compute factorial({number}), currently i={i}...")
            await asyncio.sleep(1)
            f *= i
        print(f"Task {name}: factorial({number}) = {f}")
        return f

    async def main():
        # Schedule three calls *concurrently*:
        L = await asyncio.gather(
            test.factorial("A", 2),
            test.factorial("B", 3),
            test.factorial("C", 4),
        )
        print(L)

asyncio.run(test.main())