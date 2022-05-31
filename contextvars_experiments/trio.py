from contextvars import ContextVar

import trio
import random

# https://peps.python.org/pep-0567/
opinion = ContextVar[str]("opinion")

results = []

async def extend_and_print(extension: str) -> None:
    """Print the result of adding extension to the end of the opinion ContextVar and append it to result."""
    await trio.sleep(random.random())
    opinion.set(opinion.get() + extension)
    print(opinion.get())
    results.append(opinion.get())


async def main():
    opinion.set("Python async")

    async with trio.open_nursery() as nursery:
        nursery.start_soon(extend_and_print, " is complicated")
        nursery.start_soon(extend_and_print, " has got better")
        nursery.start_soon(extend_and_print, " still isn't perfect")

    print(results)  # it would be a bit harder to get the returned values?
    print(opinion.get())


trio.run(main)
