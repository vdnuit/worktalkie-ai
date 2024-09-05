from pydantic import BaseModel


class StartConv(BaseModel):
    answer: str
