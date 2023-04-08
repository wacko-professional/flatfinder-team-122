import os
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import io

import time
import json
import numpy as np

from fastapi import FastAPI, File
from model import train, predict, convert
from pydantic import BaseModel
from typing import List, Optional

import asyncio
import concurrent.futures

from multiprocessing import Pool, cpu_count

loop = asyncio.get_event_loop()

# Class definition for parsing post response
class Data(BaseModel):
    town_filter: List[str]
    flat_type_filter: List[str]


app = FastAPI()


@app.post("/async_predict_prophet")
async def async_test_endpoint(data: Data):
    start = time.perf_counter()
    params = [{'town': town, 'flat_type': flat} for town, flat in zip(data.town_filter, data.flat_type_filter)]
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await asyncio.gather(*[loop.run_in_executor(pool, convert, p) for p in params])
    end = time.perf_counter()
    print(f"Asynchronous takes {end - start:0.4f} seconds")
    return result


@app.post("/sync_predict_prophet")
def test_endpoint(data: Data):
    start = time.perf_counter()
    params = [{'town': town, 'flat_type': flat} for town, flat in zip(data.town_filter, data.flat_type_filter)]
    result = [convert(p) for p in params]
    end = time.perf_counter()
    print(f"Synchronous takes {end - start:0.4f} seconds")
    return result