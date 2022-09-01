from pydantic import BaseModel, HttpUrl


class Image(BaseModel):
    image: HttpUrl
    name: str

    class Config:
        orm_mode = True


class ImageCreateName(BaseModel):
    name: str
    image: str


class ImageOut(ImageCreateName):
    id: int

    class Config:
        orm_mode = True
