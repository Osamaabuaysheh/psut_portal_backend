from pydantic import BaseModel, HttpUrl


class Image(BaseModel):
    image: HttpUrl
    name: str

    class Config:
        orm_mode = True


class ImageCreateName(BaseModel):
    id: int
    name: str
    image: str


class CreateStudentImage(BaseModel):
    id: int
    imageName: str
    imagePath: str


class ImageOut(ImageCreateName):
    id: int

    class Config:
        orm_mode = True
