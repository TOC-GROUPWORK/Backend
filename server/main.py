from click import Option
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
from dotenv import dotenv_values

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

class GetBrandModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    img: str = Field(...)
    models_list: list = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class GetAllBrandsModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    img: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

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
    img: Optional[str]
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
    brand_id: PyObjectId = Field(...)
    name: str = Field(...)
    link_true: Optional[str]
    link_ais: Optional[str]
    link_dtac: Optional[str]
    color_name: Optional[list]
    color_style: Optional[list]
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

class UpdateModelModel(BaseModel):
    link_true: Optional[str]
    link_ais: Optional[str]
    link_dtac: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ProviderModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    model_id: PyObjectId = Field(...)
    provider: str = Field(...)

    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class DetailModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    provider_id: PyObjectId = Field(...)
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
    model_detail_id: PyObjectId = Field(...)
    name: str = Field(...)
    detail: str = Field(...)

    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PackageModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    package_no: str = Field(...)
    promotion_id: PyObjectId = Field(...)
    specialprice: str = Field(...)
    prepaid: str = Field(...)
    package: str = Field(...)
    package_type: str = Field(...)
    package_detail: Optional[str]

    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

@app.get("/")
async def get_app():
    return { 'message': 'WongNok'}

@app.get("/brands", response_description="List all brands", response_model=List[GetAllBrandsModel])
async def list_brands():
    brands = await db["brands"].find().to_list(1000)
    return brands

@app.get("/brand/{id}", response_description="Get brand", response_model=GetBrandModel)
async def get_brand(id: str):
    brand = await db["brands"].find_one({'_id': id})
    brand['models_list'] = brand.get('models_list', await db["models"].find({'brand_id': id}, {'_id': 1, 'name': 1, 'img': 1}).to_list(1000))
    return brand

@app.post("/brand", response_description="Add new brand", response_model=BrandModel)
async def creat_brand(brand: BrandModel = Body(...)):
    if (get_brand := await db["brands"].find_one({"name": brand.name})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_brand)
    
    brand = jsonable_encoder(brand)
    new_brand = await db["brands"].insert_one(brand)
    create_brand = await db["brands"].find_one({"_id": new_brand.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_brand)

# @app.get("/brand/{id}", response_description="Get brand", response_model=BrandModel)
# async def get_brand(id: str):
#     brand = await db["brands"].find_one({'_id': id})
#     return brand


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

@app.get("/models", response_description="List all models", response_model=List[ModelModel])
async def list_models():
    models = await db["models"].find().to_list(1000)
    return models

# @app.get("/model/{id}", response_description="List all models", response_model=List[ModelModel])
# async def get_model(id: str):
#     model = await db["models"].find_one({"_id": id}
#     for provider in db["providers"].fine({'model_id': id}):
#         model[provider['provider']] 
#     return brands

@app.post("/model", response_description="Add new model", response_model=ModelModel)
async def create_model(model: ModelModel = Body(...)):
    if (get_model := await db["models"].find_one({"name": model.name})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_model)
    
    model = jsonable_encoder(model)
    new_model = await db["models"].insert_one(model)
    create_model = await db["models"].find_one({"_id": new_model.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_model)

@app.put("/model/{id}", response_description="Update a model", response_model=ModelModel)
async def update_model(id: str, model: UpdateModelModel = Body(...)):
    model = {k: v for k, v in model.dict().items() if v is not None}

    if len(model) >= 1:
        update_result = await db["models"].update_one({"_id": id}, {"$set": model})

        if update_result.modified_count == 1:
            if (
                update_model := await db["models"].find_one({"_id": id})
            ) is not None:
                return update_model

    # db["models"].update_many({"_id": id}, {"$unset": { 'link': "" }})
    if (existing_model := await db["models"].find_one({"_id": id})) is not None:
        return existing_model

    raise HTTPException(status_code=404, detail=f"Brand {id} not found")

@app.post("/provider", response_description="Add new provider", response_model=ProviderModel)
async def create_provider(provider: ProviderModel = Body(...)):
    if (get_provider := await db["providers"].find_one({"model_id": provider.model_id, 'provider': provider.provider})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_provider)
    
    provider = jsonable_encoder(provider)
    new_provider = await db["providers"].insert_one(provider)
    create_provider = await db["providers"].find_one({"_id": new_provider.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_provider)

@app.post("/detail", response_description="Add new model detail", response_model=DetailModel)
async def create_detail(detail: DetailModel = Body(...)):
    if (get_detail := await db["details"].find_one({"provider_id": detail.provider_id, 'ram': detail.ram})) is not None:
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

