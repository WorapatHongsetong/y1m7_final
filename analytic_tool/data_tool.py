import os, datetime
import numpy as np


def record(user: str, score: int, living_time):
    log = f"{datetime.datetime.now(), user, score, living_time}"
    os.system(f"echo {log} >> ''")
    