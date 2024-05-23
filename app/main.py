from fastapi import FastAPI
import uvicorn
from nlp_controler import router as nlp_model_router
from transcriptor import router as transcription_router

app = FastAPI(title="RFA Ml backend server")

app.include_router(transcription_router)
app.include_router(nlp_model_router)


