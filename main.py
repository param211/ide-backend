import csv
import json
import sqlite3
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import shlex
from subprocess import Popen, PIPE


# Start app and server
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# root
@app.get("/")
def read_root():
    return {"hello world"}


@app.post("/python/execute")
async def execute_python(request: Request):
    f = open("execute-this.py", "w")
    b = await request.body()
    program = b.decode()
    f.write(program)
    f.close()

    cmd = "python execute-this.py"

    # https: // stackoverflow.com / a / 21000308 / 12153295
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode

    return {"exitcode": exitcode, "output": out, "error": err}
