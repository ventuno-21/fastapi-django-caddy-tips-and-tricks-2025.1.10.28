from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from FastAPI app ONE !"}

@app.get("/users")
def users():
    return {"users": ["Alma", "Farbod"]}

@app.get("/health")
def health():
    return {"status": "ok"}