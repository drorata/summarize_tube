from pydantic import BaseModel


class SummeryTube(BaseModel):
    title: str
    description: str
    hashtags: list[str]
