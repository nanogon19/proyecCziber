import os
import re
import fitz
import panda as pd
import matplotlib.pyplot as plt

from backend.app.models.query import Query
from backend.app.extensions import db

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from sqlalchemy import create_engine, inspect, text
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

openai = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
connection_string = os.getenv(
    "DATABASE_URL"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=true"
    "&Encrypt=no"
    )

engine = create_engine(connection_string, connect_args={"connect_timeout": 5})

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

