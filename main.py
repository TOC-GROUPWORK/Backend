from fastapi import FastAPI, Response
import regex.Ais.ais as ais

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Connect Backend server TOC"}

@app.get("/ais/apple/{number_id}")
async def get_apple(number_id: int):
    return ais.get_iphone(number_id)

@app.get("/ais/samsung/{number_id}")
async def get_ais(number_id: int):
    return ais.get_samsung(number_id)

@app.get("/ais/huawei/{number_id}")
async def get_ais(number_id: int):
    return ais.get_huawei(number_id)

@app.get("/ais/oppo/{number_id}")
async def get_ais(number_id: int):
    return ais.get_oppo(number_id)

@app.get("/ais/vivo/{number_id}")
async def get_ais(number_id: int):
    return ais.get_vivo(number_id)

@app.get("/ais/realme/{number_id}")
async def get_ais(number_id: int):
    return ais.get_realme(number_id)

@app.get("/ais/xiaomi/{number_id}")
async def get_ais(number_id: int):
    return ais.get_xiaomi(number_id)

@app.get("/ais/oneplus/{number_id}")
async def get_ais(number_id: int):
    return ais.get_oneplus(number_id)

@app.get("/ais/asus/{number_id}")
async def get_ais(number_id: int):
    return ais.get_asus(number_id)

@app.get("/ais/ruio/{number_id}")
async def get_ais(number_id: int):
    return ais.get_ruio(number_id)
