from database import Base
from sqlalchemy import column, Integer, String, Boolean


class todos(Base):
    __tablaename__ = "todos"


id = column(Integer, primary_key=True, index=True)
title = column(String)
description = column(String)
priority = column(Integer)
complete = column(Boolean, default=False)
