
import IPython
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload
from .db import models
from imp import reload

def main():
    engine = create_engine(os.environ["DATABASE_URL"])
    with Session(engine) as session:
        IPython.embed()
