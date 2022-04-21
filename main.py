import string
from fastapi import FastAPI, Response
import regex.Ais.ais as ais
import regex.Dtac.dtac as dtac

app = FastAPI()

@app.get("/api/")
async def root():
    return {"message": "Connect Backend server TOC"}

@app.get("/api/ais/apple/{number_id}")
async def get_apple(number_id: int):
    return ais.get_iphone(number_id)

@app.get("/api/ais/samsung/{number_id}")
async def get_ais(number_id: int):
    return ais.get_samsung(number_id)

@app.get("/api/ais/huawei/{number_id}")
async def get_ais(number_id: int):
    return ais.get_huawei(number_id)

@app.get("/api/ais/oppo/{number_id}")
async def get_ais(number_id: int):
    return ais.get_oppo(number_id)

@app.get("/api/ais/vivo/{number_id}")
async def get_ais(number_id: int):
    return ais.get_vivo(number_id)

@app.get("/api/ais/realme/{number_id}")
async def get_ais(number_id: int):
    return ais.get_realme(number_id)

@app.get("/api/ais/xiaomi/{number_id}")
async def get_ais(number_id: int):
    return ais.get_xiaomi(number_id)

@app.get("/api/ais/oneplus/{number_id}")
async def get_ais(number_id: int):
    return ais.get_oneplus(number_id)

@app.get("/api/ais/asus/{number_id}")
async def get_ais(number_id: int):
    return ais.get_asus(number_id)

@app.get("/api/ais/ruio/{number_id}")
async def get_ais(number_id: int):
    return ais.get_ruio(number_id)

@app.get("/api/dtac/{brand}")
async def get_dtac(brand: str):
    return dtac.scraping(brand=brand)