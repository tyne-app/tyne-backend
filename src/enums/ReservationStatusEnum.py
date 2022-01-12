import enum


class ReservationStatusEnum(enum.Enum):
    reserva_iniciada = 1
    reserva_en_proceso = 2
    reserva_con_problemas = 3
    pago_exitoso = 4
    pago_cancelado = 5
    pago_rechazado = 6
    cancelado_local = 7
    reserva_confirmada = 8
    reserva_atendida = 9