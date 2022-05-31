from contextvars import ContextVar

import asyncio
import random

# https://peps.python.org/pep-0567/
opinion = ContextVar[str]("opinion")


async def extend_and_print(extension: str) -> str:
    """Print and return the result of adding extension to the end of the opinion ContextVar."""
    await asyncio.sleep(random.random())
    opinion.set(opinion.get() + extension)
    print(opinion.get())
    return opinion.get()


async def main():
    opinion.set("Python async")

    results = await asyncio.gather(
        extend_and_print(" is complicated"),
        extend_and_print(" has got better"),
        extend_and_print(" still isn't perfect"),
    )

    print(results)
    print(opinion.get())


# https://tenthousandmeters.com/blog/python-behind-the-scenes-12-how-asyncawait-works-in-python/
asyncio.run(main())
