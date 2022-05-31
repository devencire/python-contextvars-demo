from contextvars import ContextVar, copy_context

import asyncio
import random

opinion = ContextVar[str]("opinion")


async def extend_and_print(extension: str) -> str:
    """Print and return the result of adding extension to the end of the opinion ContextVar."""
    # spend some time sleeping
    # (this should guarantee the print order is non-deterministic)
    await asyncio.sleep(random.random())
    # set the opinion ContextVar — this only applies to the _current context_
    opinion.set(opinion.get() + extension)
    # print whatever the opinion ContextVar now holds according to the _current context_
    print(f"opinion.get() according to extend_and_print(\"{extension}\"): {opinion.get()}")
    # print (a copy of) the whole _current context_
    print(f"copy_context() according to extend_and_print(\"{extension}\"): {list(copy_context().items())}")
    # return whatever the opinion ContextVar now holds
    return opinion.get()


async def main():
    # print (a copy of) the whole _current context_ (it's empty)
    print(f"initial copy_context() according to main(): {list(copy_context().items())}")
    # set the opinion ContextVar — this applies to the current context
    opinion.set("Python async")
    # print (a copy of) the whole _current context_ (it's now got one thing set)
    print(f"second copy_context() according to main(): {list(copy_context().items())}")
    print("--------------------------------")
    # spawn three Tasks and wait on their completion
    results = await asyncio.gather(
        extend_and_print(" is complicated"),
        extend_and_print(" has got better"),
        extend_and_print(" still isn't perfect"),
    )
    # print the results, mostly to show how asyncio.gather works
    print("--------------------------------")
    print(f"results from the asyncio.gather(...): {results}")
    # confirm that the _current context_ hasn't been changed
    print(f"opinion.get() according to main(): {opinion.get()}")
    # print (a copy of) the whole _current context_,
    # just to confirm nothing leaked upwards
    print(f"final copy_context() according to main(): {list(copy_context().items())}")


# run an event loop with main() as its sole starting Task
asyncio.run(main())
