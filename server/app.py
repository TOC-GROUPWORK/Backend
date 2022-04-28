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

class GetBrandSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    img: str = Field(...)
    models_list: list = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class GetAllBrandsSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    img: str = Field(...)
    true: list = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class BrandSchema(BaseModel):
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

class UpdateBrandSchema(BaseModel):
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

class ModelSchema(BaseModel):
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

class GetModelSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    links: dict = Field(...)
    color_name: Optional[list]
    color_style: Optional[list]
    img: list = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UpdateModelSchema(BaseModel):
    link_true: Optional[str]
    link_ais: Optional[str]
    link_dtac: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class GetProviderSchema(BaseModel):
    details: dict = Field(...)

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
        json_encoders = {ObjectId: str}

class ProviderSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    model_id: PyObjectId = Field(...)
    provider: str = Field(...)

    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class DetailSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    provider_id: PyObjectId = Field(...)
    ram: str = Field(...)
    normalprice: Optional[str]
    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UpdateDetailSchema(BaseModel):
    normalprice: Optional[str] = Field(...)

    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PromotionSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    model_detail_id: PyObjectId = Field(...)
    name: str = Field(...)
    detail: str = Field(...)

    class Config:
        allow_population_by_field_id = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PackageSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    package_no: Optional[str]
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

@app.get("/brands", tags=["Brands"], response_description="List all brands", response_model=List[GetAllBrandsSchema])
async def list_brands():
    brands = await db["brands"].find().to_list(1000)
    for brand in brands:
        models = await db["models"].find({'brand_id':brand['_id']}, {'name': 1}).to_list(1000)
        if models == []:
            brands.remove(brand)
    return brands

@app.get("/brand/{id}", tags=["Brands"], response_description="Get brand", response_model=GetBrandSchema)
async def get_brand(id: str):
    brand = await db["brands"].find_one({'_id': id})
    brand['models_list'] = brand.get('models_list', await db["models"].find(
        {"$and": [
            {'brand_id': id}, 
            {'img': {
                    "$ne": []
                }}
        ]},
        {'_id': 1, 'name': 1, 'img': 1}).to_list(1000))
    return brand

@app.post("/brand", tags=["Brands"], response_description="Add new brand", response_model=BrandSchema)
async def creat_brand(brand: BrandSchema = Body(...)):
    if (get_brand := await db["brands"].find_one({"name": brand.name})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_brand)
    
    brand = jsonable_encoder(brand)
    new_brand = await db["brands"].insert_one(brand)
    create_brand = await db["brands"].find_one({"_id": new_brand.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_brand)

# @app.get("/brand/{id}", response_description="Get brand", response_model=BrandSchema)
# async def get_brand(id: str):
#     brand = await db["brands"].find_one({'_id': id})
#     return brand


@app.put("/brand/{id}", tags=["Brands"], response_description="Update a brand", response_model=BrandSchema)
async def update_brand(id: str, brand: UpdateBrandSchema = Body(...)):
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

@app.get("/models", tags=["Models"], response_description="List all models", response_model=List[ModelSchema])
async def list_models():
    models = await db["models"].find().to_list(1000)
    return models

@app.get("/model/{model_id}", tags=["Models"], response_description="Get model", response_model=GetModelSchema)
async def get_model(model_id: str):
    model = await db["models"].find_one({"_id": model_id}, {'brand_id': 0})
    model['links'] = dict()
    model['links']['TRUE'] = model['link_true']
    # model['links']['AIS'] = model['link_ais']
    # model['links']['DTAC'] = model['link_dtac']
    
    return model

@app.post("/model", tags=["Models"], response_description="Add new model", response_model=ModelSchema)
async def create_model(model: ModelSchema = Body(...)):
    if (get_model := await db["models"].find_one({"name": model.name})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_model)
    
    model = jsonable_encoder(model)
    new_model = await db["models"].insert_one(model)
    create_model = await db["models"].find_one({"_id": new_model.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_model)

@app.put("/model/{id}", tags=["Models"], response_description="Update a model", response_model=ModelSchema)
async def update_model(id: str, model: UpdateModelSchema = Body(...)):
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

@app.get("/provider/{model_id}", tags=["Providers"], response_description="Get providers", response_model=List[ProviderSchema])
async def get_providers(model_id: str, provider: GetProviderSchema = Body(...)):
    providers = await db["providers"].find({'model_id': model_id}).to_list(1000)

    return providers

@app.get("/provider/{provider_name}/{model_id}", tags=["Providers"], response_description="Get providers", response_model=GetProviderSchema)
async def get_providers(provider_name: str, model_id: str):
    print(provider_name, model_id)
    details = dict()
    for provider in await db["providers"].find({'model_id': model_id, 'provider': provider_name}).to_list(1000):
        # if details.get(provider_name, {}) != {} and provider_name == "TRUE":
        #     continue
        details[provider_name] = details.get(provider_name, {})
        for detail in await db["details"].find({'provider_id': provider['_id']}, {'provider_id': 0}).to_list(1000):
            
            detail['promotions'] = list()
            for promotion in await db["promotions"].find({'model_detail_id': detail['_id']}, {'model_detail_id': 0}).to_list(1000):
                packages = await db["packages"].find({'promotion_id': promotion['_id']}, {'promotion_id': 0, 'package_no': 0}).to_list(1000)
                promotion['packages'] = packages
                detail['promotions'].append(promotion)
            
            if details[provider_name].get(detail['ram'], []) == []:
                details[provider_name][detail['ram']] = detail
    return { 'details' : details }

@app.post("/provider", tags=["Providers"], response_description="Add new provider", response_model=ProviderSchema)
async def create_provider(provider: ProviderSchema = Body(...)):
    if (get_provider := await db["providers"].find_one({"model_id": provider.model_id, 'provider': provider.provider})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_provider)
    
    provider = jsonable_encoder(provider)
    new_provider = await db["providers"].insert_one(provider)
    create_provider = await db["providers"].find_one({"_id": new_provider.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_provider)

@app.get("/detail/{provider_id}", tags=["Details"], response_description="Get details", response_model=List[DetailSchema])
async def get_details(provider_id: str):
    details = await db["details"].find({'provider_id': provider_id}).to_list(1000)
    return details

@app.post("/detail", tags=["Details"], response_description="Add new model detail", response_model=DetailSchema)
async def create_detail(detail: DetailSchema = Body(...)):
    if (get_detail := await db["details"].find_one({"provider_id": detail.provider_id, 'ram': detail.ram})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_detail)
    
    detail = jsonable_encoder(detail)
    new_detail = await db["details"].insert_one(detail)
    create_detail = await db["details"].find_one({"_id": new_detail.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_detail)

@app.put("/detail/{id}", tags=["Details"], response_description="Update a model detail", response_model=DetailSchema)
async def update_detail(id: str, detail: UpdateDetailSchema = Body(...)):
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

@app.get("/promotion/{detail_id}", tags=["Promotions"], response_description="Get promotions", response_model=List[PromotionSchema])
async def get_promotions(detail_id: str):
    promotions = await db["promotions"].find({'model_detail_id': detail_id}).to_list(1000)
    return promotions

@app.post("/promotion", tags=["Promotions"], response_description="Add new promotion", response_model=PromotionSchema)
async def create_promotion(promotion: PromotionSchema = Body(...)):
    if (get_promotion := await db["promotions"].find_one({"model_detail_id": promotion.model_detail_id, 'name': promotion.name})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_promotion)
    
    promotion = jsonable_encoder(promotion)
    new_promotion = await db["promotions"].insert_one(promotion)
    create_promotion = await db["promotions"].find_one({"_id": new_promotion.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_promotion)

@app.get("/package/{promotion_id}", tags=["Packages"], response_description="Get packages", response_model=List[PackageSchema])
async def get_packages(promotion_id: str):
    packages = await db["packages"].find({'promotion_id': promotion_id}).to_list(1000)
    return packages

@app.post("/package", tags=["Packages"], response_description="Add new package", response_model=PackageSchema)
async def create_package(package: PackageSchema = Body(...)):
    if (get_package := await db["packages"].find_one({"package_no": package.package_no, 'promotion_id': package.promotion_id})) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=get_package)
    
    package = jsonable_encoder(package)
    new_package = await db["packages"].insert_one(package)
    create_package = await db["packages"].find_one({"_id": new_package.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_package)

