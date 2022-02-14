import threading

# TODO: Eliminar
class ReservationEvent(threading.Timer):
    def __init__(self, reservation_id: int):
        threading.Timer.__init__(self, interval=15, function=self.long_running_task)
        self.reservation_id = reservation_id

    def long_running_task(self):
        print("Fin hilo se anula reserva: " + str(self.reservation_id))
        # TODO: Llamar funcion para anular reserva y enviar correo cliente/local

    @classmethod
    def check_thread(cls, reservation_id: str): # TODO: ID reserva debe ser int
        for thread in threading.enumerate():
            if isinstance(thread, ReservationEvent):
                if thread.reservation_id == int(reservation_id): # TODO: ID reserva debe ser int
                    print("Hilo encontrado: " + str(thread.reservation_id))
                    print("Se corta ejecución")
                    thread.cancel()
                    # TODO: Llamar actualizar reserva y confirmar con email cliente/local
        return "No encontrado"