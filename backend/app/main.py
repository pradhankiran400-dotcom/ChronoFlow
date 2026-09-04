from fastapi import FastAPI

app = FastAPI()
app.title = "ChronoFlow API"

@app.get("/")
def home():
    return {
        "message": "Welcome to the ChronoFlow API!"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }