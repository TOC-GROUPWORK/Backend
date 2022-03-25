from fastapi import FastAPI

app = FastAPI()


@app.get("/true")
async def read_item():
    return 
