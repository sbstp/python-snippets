import random

from retry import retry


def prone_to_errors():
    if random.random() <= 0.95:
        raise ValueError
    return "hello"


@retry(0.25, timeout=2, max_attempts=6)
def retry_prone_to_errors():
    while True:
        try:
            return prone_to_errors()
        except ValueError:
            print("Error!")
            yield


print("Success:", retry_prone_to_errors())
