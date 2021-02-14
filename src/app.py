import os
import pathlib
from functools import lru_cache
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from .airtable import Airtable
BASE_DIR = pathlib.Path(__file__).parent
app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR/'templates')


@lru_cache()
def cached_dotenv():
    load_dotenv(verbose=True)


cached_dotenv()
base_id = os.getenv("AIRTABLE_BASE_ID")
api_key = os.getenv("AIRTABLE_API_KEY")
table_name = os.getenv("AIRTABLE_TABLE_NAME")


@app.get("/")
def home_view(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})


@app.post("/")
def home_signup_view(request: Request, email: str = Form(...)):
    '''
    TODO add CSRF for security
    '''
    # Send email to airtable
    airtable_client = Airtable(
        base_id=base_id,
        api_key=api_key,
        table_name=table_name
    )
    print(airtable_client)
    did_send = airtable_client.create_records({"email":email})
    print(did_send)
    return templates.TemplateResponse('home.html', {"request": request, "submitted_email": email, "did_send": did_send})
