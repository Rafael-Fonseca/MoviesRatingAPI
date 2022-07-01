from fastapi import FastAPI

app = FastAPI()

#  postgress EDB pgadmin
@app.get("/")
async def root():
    return {"message": "Hello World"}
