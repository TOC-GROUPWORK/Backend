from fastapi import FastAPI, Response
import regex.Ais.ais as ais

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ais")
async def get_ais(response: Response):
    # response.headers["charset"] = "utf-8"
    return ais.get_iphone_5g()

