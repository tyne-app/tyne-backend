class Constants:
    # ERRORS MESSAGES
    INTERNAL_ERROR = "INTERNAL SERVER ERROR"
    INTERNAL_ERROR_DETAIL = "Ha ocurrido un error, por favor inténtelo de nuevo más tarde"

    MENU_READ_ERROR = "Error al obtener menu"
    MENU_READ_ERROR_DETAIL = "Productos no encontrados para el menu"
    MENU_CREATE_ERROR = "Error al crear menu"
    MENU_CREATE_ERROR_DETAIL = "Error al guardar los productos para el menu"
    MENU_ALL_CATEGORY_ERROR = "Error al obtener categorias"
    MENU_ALL_CATEGORY_ERROR_DETAIL = "Categorias no encontradas para el menu"

    BANK_READ_ERROR = "Error al obtener banco"
    BANK_READ_ERROR_DETAIL = "Banco no encontrados"

    BRANCH_READ_ERROR = "Error al obtener branch"
    BRANCH_NOT_FOUND_ERROR_DETAIL = "Branch no encontrado"
    BRANCH_ADD_ERROR = "Error al agregar branch"
    BRANCH_DAY_UNABLE = "Error día no válido"
    BRANCH_DAY_UNABLE_DETAIL = "Día no disponible/registrado para la sucursal"
    BRANCH_MAX_RESERVATION = "Sucursal con máximo de reservas"

    MANAGER_NOT_FOUND_ERROR_DETAIL = "Manager no encontrado"

    CLIENT_NOT_FOUND_ERROR_DETAIL = "Cliente no encontrado"
    CLIENT_CREATE_ERROR_DETAIL = "Cliente no pudo ser creado"
    CLIENT_NOT_EXIST = "Cliente no existen"

    USER_NO_AUTH = "Usuario no autorizado"
    USER_NO_AUTH_DETAIL = "X"
    USER_EMAIL_EXIST = "Usuario con el email ya existe"
    USER_ALREADY_EXIST = "Usuario ya existe en el sistema"
    USER_EXIST_FIREBASE = "Usuario registrado con redes sociales"
    USER_CREATE_ERROR = "Error al crear usuario"
    USER_TYPE_MOT_FOUND = "Tipo de usuario no encontrado"
    USER_NOT_FOUND = "Usuario no encontrado"
    USER_NOT_FOUND_DETAIL = "No existe usuario en el sistema"
    USER_NOT_EXIST = "Usuario no existen"
    USER_NOT_IMAGE_ERROR = "Usuario no posee imagen de perfil"

    ACCOUNT_PROFILE_GET_ERROR = "Error al obtener el perfil"
    ACCOUNT_PROFILE_ERROR = "Error get_account_profile"

    FIELDS_VALIDATOR_ERROR = "Los datos no son validos"

    SIGNATURE_EXPIRED_MSG = "Token expirado"
    ALGORITHM_MSG = "Token entrante no permitido"
    TOKEN_DECODE_ERROR = "Error al decodificar token"
    TOKEN_VERIFY_ERROR = "Error al verificar token"
    TOKEN_INVALID_ERROR = "Token invalido"
    TOKEN_NOT_EXIST = "Token no existe"
    TOKEN_NOT_EXIST_DETAIL = "Debe autenticarse para utilizar el servicio"

    RESERVATION_DATE_INVALID_ERROR = "Fecha para reserva no válida"
    RESERVATION_DATETIME_DESCRIPTION_ERROR = "Fecha de reserva no puede estar fijado para el pasado"
    RESERVATION_DATE_DESCRIPTION_ERROR = "Fecha debe ser día disponible dentro de una semana"
    RESERVATION_TIME_INVALID_ERROR = "Hora para reserva no válida"
    RESERVATION_TIME_DESCRIPTION_ERROR = "Hora de reserva debe tener diferencia de 2hrs mínimo dentro de horario de local"
    RESERVATION_REQUEST_TIME_DESCRIPTION_ERROR = "Debe haber 2 hrs mínimo de diferencia entre solicitud y reserva"
    RESERVATION_GET_ERROR = "Error al obtener reservas"
    RESERVATION_NOT_FOUND_ERROR = "Reservas no encontradas"

    COUNTRY_NOT_FOUND_ERROR = "Paises no encontrados"
    CITIES_NOT_FOUND_ERROR = "Ciudades no encontrados"

    STATES_NOT_FOUND_ERROR = "Estados no encontrados"

    PRODUCT_NOT_EXIST = "No existen productos"
    CLIENT_UNAUTHORIZED = "Cliente no autorizado"
    BUY_INVALID_ERROR = "Compra no válida"
    MP_GET_ERROR: str = "Error obtener datos mercado pago"

    INVALID_DATA_ERROR = "Datos inválidos"

    DATE_EMPTY_ERROR = "Fecha de reserva no puede estar vacia"

    PAGE_LEN_ERROR = "N° de página debe ser mayor a 0"

    RESULT_PAGE_LEN_ERROR = "Resultado por página debe ser mayor a 0"

    STATUS_RESERVATION_LEN_ERROR = "Estado de la reserva debe ser mayor a 0"

    EMAIL_INVALID_ERROR = "Email no es válido"

    PASSWORD_EMPTY_ERROR = "Contraseña no puede estar vacia"
    PASSWORD_INVALID_ERROR = "Contraseña inválida"

    PEOPLE_FIELD_LEN_ERROR = "Campo people debe ser mayor a 0 y menor a 11"

    LOGIN_ERROR = "Error al iniciar sesión"

    GEO_DECODE_ERROR = "Error de geocodificación"
    GEO_COORDENATES_EMPTY_ERROR = "No hay datos geocodificados"

    CREDENTIALS_CREATE_ERROR = "Error al crear redenciales"

    IMAGE_DELETE_ERROR = "Error eliminar imagen"
    IMAGE_UPLOAD_ERROR = "Error al subir imagen"
    IMAGE_NOT_FOUND_ERROR = "Imagen no encontrada"

    CLIENT = 'client'
    BRANCH = 'branch'
    USER = 'user'
