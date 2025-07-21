from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routers.whatsapp import router as whatsapp_router

app = FastAPI()

app.include_router(whatsapp_router)

@app.get("/")
def read_root():
    return {"message": "WhatsApp bot API running..."}


# RUN
# source venv/bin/activate
# pip install -r requirements.txt
# uvicorn main:app --reload
# ngrok http http://localhost:8000       

# docker build -t fastapi-app .
# docker run -p 8000:8000 fastapi-app