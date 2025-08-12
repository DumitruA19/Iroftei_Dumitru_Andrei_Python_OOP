from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import math
from auth import auth 
from monitor import monitor
import logging 
from pythonjsonlogger import jsonlogger
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creează tabele
Base.metadata.create_all(bind=engine)



app.include_router(auth.router)
app.include_router(math.router)
app.include_router(monitor, prefix="/monitor")
app.mount("/", StaticFiles(directory="dist", html=True), name="static")

logger = logging.getLogger("fastapi_logger")
logger.setLevel(logging.INFO)

# Configurează handlerul pentru console (stdout)
log_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s'
)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)