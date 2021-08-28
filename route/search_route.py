from fastapi import status,APIRouter, Response
from fastapi.params import Depends
from typing import Optional
from loguru import logger
from schema.search_schema import SearchParameters

search_router = APIRouter(
    prefix="/v1/api/search",
    tags=["Search"]
)

@search_router.post('/all-branch')
def search_locals(search_parameters: SearchParameters):
    logger.info('search_paramters: {}', search_parameters)
    return True