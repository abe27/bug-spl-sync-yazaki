from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class GediModel(BaseModel):
    id: int  # integer primary key autoincrement,
    objtype: str  # text not null,
    mailbox: str  # text not null,
    batchid: str  # text not null unique,
    size: float  # real,
    batchfile: str  # text,
    currentdate: int  # numeric,
    flags: str  # text,
    formats: str  # text,
    orgname: str  # text,
    factory: str  # text,
    filetype: str  # text,
    download: int  # integer,
    destination: str  # text,
    linkfile: str  # text)"""


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
