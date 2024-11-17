import os
from dotenv import load_dotenv
from fastapi import FastAPI
from routers import api_router

load_dotenv(".env")

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
