from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/users")
def users():
    return {"users": ["Alice", "Bob", "Charlie"]}

@app.get("/health")
def health():
    return {"status": "ok"}