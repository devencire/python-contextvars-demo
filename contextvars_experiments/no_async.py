from contextvars import ContextVar, copy_context

import random
import time

opinion = ContextVar[str]("opinion")


def extend_and_print(extension: str) -> str:
    """Print and return the result of adding extension to the end of the opinion ContextVar."""
    time.sleep(random.random())
    opinion.set(opinion.get() + extension)
    print(opinion.get())
    return opinion.get()


def main():
    opinion.set("Python sync")

    results = [
        copy_context().run(extend_and_print, " is hampered by the GIL"),
        copy_context().run(extend_and_print, " is easier to reason about"),
        copy_context().run(extend_and_print, " is hard to escape"),
    ]

    print(results)
    print(opinion.get())


main()
