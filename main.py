from fastapi import FastAPI
from backend.routes.textprocess import router as tp
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.include_router(tp)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Akash API. Visit /docs for API documentation."}
