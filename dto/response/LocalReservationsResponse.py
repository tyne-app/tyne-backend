import math
from datetime import datetime


class LocalReservations:
    reservation_id: int
    client_id: int
    name: str
    last_name: str
    preference: str
    reservation_date: datetime
    reservation_date_status: datetime
    hour: str
    status_id: str
    status_description: str
    people: int
    street: str
    street_number: int
    state: str
    city: str
    country: str


class LocalReservationsDate:
    reservation_date: datetime
    reservation_week_day: str
    reservation_pending: int
    reservation_confirmed: int
    reservation_attended: int
    reservation_canceled: int
    local_reservations: list[LocalReservations]


class LocalReservationsResponse:
    total_items: int
    total_items_page: int
    page: int
    total_pages: int
    local_reservations_date: list[LocalReservationsDate]

    @classmethod
    def local_reservations(cls, localReservations: list, localReservationsDate: list, result_for_page: int,
                           page_number: int):

        reservations_response = LocalReservationsResponse()
        local_reservations_date_list: list[LocalReservationsDate] = []
        total_items: int = 0
        for idxDate, local_reservations_date in enumerate(localReservationsDate):
            local_reservations_list: list[LocalReservations] = []
            local_reservations_date_obj = LocalReservationsDate()
            reservation_date_local_reservation_date: datetime = local_reservations_date.reservation_date

            reservation_attended: int = 0
            reservation_confirmed: int = 0
            reservation_canceled: int = 0
            reservation_pending: int = 0
            if idxDate == 0:
                total_items = local_reservations_date.total_items

            for idx, local_reservations in enumerate(localReservations):
                reservation_date_local_reservation: datetime = local_reservations.reservation_date

                if reservation_date_local_reservation.day == reservation_date_local_reservation_date.day:
                    local_reservations_obj = LocalReservations()
                    local_reservations_obj.reservation_id = local_reservations.id
                    local_reservations_obj.name = local_reservations.name
                    local_reservations_obj.last_name = local_reservations.last_name
                    local_reservations_obj.preference = local_reservations.preference
                    local_reservations_obj.reservation_date = local_reservations.reservation_date
                    local_reservations_obj.reservation_date_status = local_reservations.reservation_date_status
                    local_reservations_obj.hour = local_reservations.hour
                    local_reservations_obj.people = local_reservations.people
                    local_reservations_obj.status_id = local_reservations.status_id
                    local_reservations_obj.status_description = local_reservations.status_description
                    local_reservations_obj.street = local_reservations.street
                    local_reservations_obj.street_number = local_reservations.street_number
                    local_reservations_obj.state = local_reservations.state
                    local_reservations_obj.city = local_reservations.city
                    local_reservations_obj.country = local_reservations.country

                    if local_reservations_obj.status_id == 4:
                        reservation_pending += 1

                    if local_reservations_obj.status_id == 7:
                        reservation_canceled += 1

                    if local_reservations_obj.status_id == 8:
                        reservation_confirmed += 1

                    if local_reservations_obj.status_id == 9:
                        reservation_attended += 1

                    local_reservations_list.append(local_reservations_obj)
            if len(local_reservations_list) > 0:
                local_reservations_date_obj.reservation_date = local_reservations_date.reservation_date
                local_reservations_date_obj.reservation_week_day = local_reservations_date.reservation_date.strftime("%A")
                local_reservations_date_obj.reservation_attended = reservation_attended
                local_reservations_date_obj.reservation_confirmed = reservation_confirmed
                local_reservations_date_obj.reservation_canceled = reservation_canceled
                local_reservations_date_obj.reservation_pending = reservation_pending
                local_reservations_date_obj.local_reservations = local_reservations_list
                local_reservations_date_list.append(local_reservations_date_obj)

        if len(local_reservations_date_list) > 0:
            reservations_response.total_items = total_items
            reservations_response.page = page_number
            reservations_response.total_items_page = result_for_page
            reservations_response.total_pages = math.ceil(total_items / result_for_page)

            reservations_response.local_reservations_date = local_reservations_date_list

        return reservations_response
