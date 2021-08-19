from fastapi import APIRouter, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# TODO: No sé si lo vaya a ocupar

routes = APIRouter()

'''
@routes.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    pass

'''
@routes.get("/show/restaurants/") # TODO: Falta parámetro
def show_restaurants():
    pass


@routes.get("/show/branchs/") # TODO: Falta parámetro
def show_branch():
    pass


@routes.get("/show/schedules/") # TODO: Falta parámetro
def show_schedules():
    pass


@routes.get('/show/schedule/{schedule_id}')
def show_schedule_details(schedule_id: int):
    return "ok"


@routes.get('/show/image/{id_image}')
def show_image_details():
    pass


@routes.get('/show/restaurant/{restaurant_id}')
def show_restaurant_details():
    pass


@routes.get('/show/branch/{branch_id}')
def show_branch_details():
    pass


@routes.get('/show/representativelegal/{representative_id}')
def show_representative_legal_details():
    pass


@routes.post("/add/image/")
def create_image():
    pass


@routes.post('/add/schedule/')
def add_schedule():
    pass


@routes.post('/add/legalrepresentative/')
def register_representative():
    pass


@routes.post('/add/bank/')
def register_bank():
    pass


@routes.post('/add/restaurant/')
def register_restaurant():
    pass


@routes.post('/add/branch/')
def create_branch():
    pass


@routes.delete('/delete/image/{image_id}')
def delete_image():
    pass


@routes.delete('/delete/restaurant/{restaurant_id}')
def delete_restaurant():
    pass


@routes.delete('/delete/schedule/{schedule_id}')
def delete_schedule():
    pass


@routes.delete('/delete/bank/{bank_id}')
def delete_bank_restaurant():
    pass


@routes.delete('/delete/branch/{branch_id}')
def delete_branch():
    pass


@routes.put('/update/restaurant/{restaurant_id}')
def update_restaurant():
    pass


@routes.put('/update/legalrepresentative/{representative_id}')
def update_representative_legal():
    pass


@routes.put('/update/branch/{id_branch}')
def update_branch():
    pass


@routes.put('/update/image/{image_id}')
def update_image():
    pass


@routes.put('/update/schedule/{schedule_id}')
def update_schedule():
    pass
