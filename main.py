from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"status": "Nima is active", "message": "Hello World"}
