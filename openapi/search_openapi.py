class SearchAllBranchOpenAPI:
    summary = "Busca y filtra locales"
    description = "Busca y filtra los locales según parámetros opcionales que se obtienen "
    response_description = "Retorna listado de locales filtrados dentro de key data, si ocurre algún error " \
                           "se retorna data vacía y en key error descripción."
    responses = {
        200: {"content": {"application/json": {"example": {'data': [
        {
            "id": 1,
            "name": "La picá del Rick",
            "image_url": None,
            "amount_avg": 3426,
            "qualification_avg": False,
            "description": "Restaurant pulento"
        },
        {
            "id": 2,
            "name": "Tuna Restobar",
            "image_url": "url_image_branch_2",
            "amount_avg": 3426,
            "qualification_avg": 4,
            "description": "Restaurant pulento"
        }], 'error': []}}}},
        400: {"description": "Error al buscar locales",
              "content": {"application/json": {"example": {'data': [], 'error': 'Error al buscar locales'}}}},
        422: {"description": "No hay validaciones de campos obligatorios para este endpoint, datos son opcionales"}
    }


class SearchAllBranchByClientOpenAPI:
    summary = "Busca y filtra locales según cliente logeado"
    description = "Busca y filtra los locales según parámetros opcionales que se obtienen "
    response_description = "Retorna listado de locales filtrados dentro de key data, si ocurre algún error " \
                           "se retorna data vacía y en key error descripción."
    responses = {
        200: {"content": {"application/json": {"example": {'data': [
        {
            "id": 1,
            "name": "La picá del Rick",
            "is_favourite": False,
            "image_url": None,
            "amount_avg": 3426,
            "qualification_avg": False,
            "description": "Restaurant pulento"
        },
        {
            "id": 2,
            "name": "Tuna Restobar",
            "is_favourite": False,
            "image_url": "url_image_branch_2",
            "amount_avg": 3426,
            "qualification_avg": 4,
            "description": "Restaurant pulento"
        }], 'error': []}}}},
        400: {"description": "Error al buscar locales",
              "content": {"application/json": {"example": {'data': [], 'error': 'Error al buscar locales'}}}},
        422: {"description": "No hay validaciones de campos obligatorios para este endpoint, datos son opcionales"}
    }