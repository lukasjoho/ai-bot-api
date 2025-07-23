from pydantic import BaseModel

class Address(BaseModel):
    street: str
    zipcode: str
    city: str

class Store(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    address: Address

class Product(BaseModel):
    id: str
    imageUrl: str
    title: str
    price: str

class Tip(BaseModel):
    id: str
    image: str
    title: str
    description: str
    url: str
    cta: str

class Question(BaseModel):
    id: str
    title: str
    description: str