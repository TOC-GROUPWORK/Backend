from fastapi import FastAPI, Response
import regex.Ais.ais as ais

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Connect Backend server TOC"}

@app.get("/ais/{number_id}")
async def get_ais(number_id: int):
    return ais.get_iphone(number_id)

