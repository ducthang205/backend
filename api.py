import json

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import create_engine
from starlette.middleware.cors import CORSMiddleware

from db import models, schema
from db.database import engine, conn
from db.models import records, condition
from db.schema import ConditionRecord

app = FastAPI()

# Dependency

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/get_record", tags=["records"])
async def get_record():
    with engine.connect() as con:
        print(con)
        rs = con.execute('SELECT * FROM records')
        list = []
        for row in rs:
            list.append(row)
        rs.close()
    return list


@app.put(
    "/set_condition/{price}/{vol}", tags=["conditions"]
)
async def set_condition(con: ConditionRecord, price: int, vol: int):
    _engine = create_engine("sqlite:///./sql_app.db")
    _conn = engine.connect()
    _conn.execute("INSERT INTO condition (price, vol) VALUES (:price, :vol)",  price=price, vol=vol)
    rs = _conn.execute('SELECT * FROM condition ORDER BY id DESC LIMIT 1')
    print(rs)
    return 1

@app.get(
    "/get_condition", tags=["conditions"], responses=schema.ConditionRecord
)
async def get_condition(con: ConditionRecord):
    _engine = create_engine("sqlite:///./sql_app.db")
    _conn = engine.connect()
    rs = _conn.execute('SELECT * FROM condition ORDER BY id DESC LIMIT 1')
    print(rs)
    return

