from fastapi import FastAPI


app = FastAPI(title="My FastAPI Project")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


