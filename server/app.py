from click import Option
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
from dotenv import dotenv_values
from enum import Enum

providers = ['AIS', 'DTAC', 'TRUE']
TypeEnum = Enum("TypeEnum", providers)

config = dotenv_values(".env")
app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(config['MONGODB_URL'])
db = client.phonepromotions

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class BrandModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    img: str = "www.google.com"
    ais: list = []
    dtac: list = []
    true: list = []

    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Tomato",
                "img": "http://example"
            }
        }

class UpdateBrandModel(BaseModel):
    ais: Optional[list]
    dtac: Optional[list]
    true: Optional[list]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                'ais': [ 'www.google.com' ],
                'dtac': [ 'www.google.com' ],
                'true': [ 'www.google.com' ]
            }
        }

class ModelModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    provider: str = Field(...)
    brand_id: PyObjectId = Field(...)
    name: str = Field(...)
    link: str = Field(...)
    img: list = Field(...)

    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                'provider': 'TRUE',
                'brand_id': '62570f9cf00fd0e5886b7f19',
                'link': 'http://example.com',
                'img': []
            }
        }

class DetailModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    model_id: str = Field(...)
    ram: str = Field(...)
    normalprice: Optional[str]
    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UpdateDetailModel(BaseModel):
    normalprice: Optional[str] = Field(...)

    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PromotionModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    model_detail_id: str = Field(...)
    name: str = Field(...)
    detail: str = Field(...)

    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PackageModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    package_no: str = Field(...)
    promotion_id: str = Field(...)
    specialprice: str = Field(...)
    prepaid: str = Field(...)
    package: str = Field(...)
    package_type: str = Field(...)

    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

@app.post("/brand", response_description="Add new brand", response_model=BrandModel)
async def creat_brand(brand: BrandModel = Body(...)):
    if (get_brand := await db["brands"].find_one({"name": brand.name})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_brand)
    
    brand = jsonable_encoder(brand)
    new_brand = await db["brands"].insert_one(brand)
    create_brand = await db["brands"].find_one({"_id": new_brand.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_brand)

@app.get(
    "/brands", response_description="List all brands", response_model=List[BrandModel]
)
async def list_brands():
    brands = await db["brands"].find().to_list(1000)
    return brands

@app.put("/brand/{id}", response_description="Update a brand", response_model=BrandModel)
async def update_brand(id: str, brand: UpdateBrandModel = Body(...)):
    brand = {k: v for k, v in brand.dict().items() if v is not None}

    if len(brand) >= 1:
        update_result = await db["brands"].update_one({"_id": id}, {"$set": brand})

        if update_result.modified_count == 1:
            if (
                update_brand := await db["brands"].find_one({"_id": id})
            ) is not None:
                return update_brand

    if (existing_brand := await db["brands"].find_one({"_id": id})) is not None:
        return existing_brand

    raise HTTPException(status_code=404, detail=f"Brand {id} not found")

@app.post("/model", response_description="Add new model", response_model=ModelModel)
async def create_model(model: ModelModel = Body(...)):
    if (get_model := await db["models"].find_one({"name": model.name})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_model)
    
    model = jsonable_encoder(model)
    new_model = await db["models"].insert_one(model)
    create_model = await db["models"].find_one({"_id": new_model.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_model)

@app.post("/detail", response_description="Add new model detail", response_model=DetailModel)
async def create_detail(detail: DetailModel = Body(...)):
    if (get_detail := await db["details"].find_one({"model_id": detail.model_id, 'ram': detail.ram})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_detail)
    
    detail = jsonable_encoder(detail)
    new_detail = await db["details"].insert_one(detail)
    create_detail = await db["details"].find_one({"_id": new_detail.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_detail)

@app.put("/detail/{id}", response_description="Update a model detail", response_model=DetailModel)
async def update_detail(id: str, detail: UpdateDetailModel = Body(...)):
    detail = {k: v for k, v in detail.dict().items() if v is not None}

    if len(detail) >= 1:
        update_result = await db["details"].update_one({"_id": id}, {"$set": detail})

        if update_result.modified_count == 1:
            if (
                update_detail := await db["details"].find_one({"_id": id})
            ) is not None:
                return update_detail

    if (existing_detail := await db["details"].find_one({"_id": id})) is not None:
        return existing_detail

    raise HTTPException(status_code=404, detail=f"Detail {id} not found")

@app.post("/promotion", response_description="Add new promotion", response_model=PromotionModel)
async def create_promotion(promotion: PromotionModel = Body(...)):
    if (get_promotion := await db["promotions"].find_one({"model_detail_id": promotion.model_detail_id, 'name': promotion.name})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_promotion)
    
    promotion = jsonable_encoder(promotion)
    new_promotion = await db["promotions"].insert_one(promotion)
    create_promotion = await db["promotions"].find_one({"_id": new_promotion.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_promotion)

@app.post("/package", response_description="Add new package", response_model=PackageModel)
async def create_package(package: PackageModel = Body(...)):
    if (get_package := await db["packages"].find_one({"package_no": package.package_no, 'promotion_id': package.promotion_id})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_package)
    
    package = jsonable_encoder(package)
    new_package = await db["packages"].insert_one(package)
    create_package = await db["packages"].find_one({"_id": new_package.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_package)

