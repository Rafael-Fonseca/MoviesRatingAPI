from fastapi import FastAPI

app = FastAPI()

#  postgress EDB
@app.get("/")
async def root():
    return {"message": "Hello World"}
