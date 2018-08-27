import time
import random
import uuid


def randomTime():
    return long(round(time.time() * 1000)) + random.randint(0, 100000)


# return an unique string
def randomUuid():
    return uuid.uuid4()
