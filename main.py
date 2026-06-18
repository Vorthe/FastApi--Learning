from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Vorthe is active", "message": "API is running perfectly"}