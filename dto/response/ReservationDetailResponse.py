import datetime


class ReservationDetail:
    category_id: int
    name_product: str
    product_description: str
    product_amount: str
    product_quantity: str


class ReservationDetailResponse:
    reservation_id: int
    reservation_week_day: str
    people: int
    street: str
    street_number: str
    state: str
    city: str
    country: str
    preference: str
    reservation_date: datetime
    hour: str
    total_price: int
    name: str;
    last_name: str;
    reservation_detail: list[ReservationDetail]

    @classmethod
    def reservation_detail(cls, reservationDetail: list):
        reservations_detail_response = ReservationDetailResponse()

        reservation_detail_list: list[ReservationDetail] = []
        total_price: int = 0
        for idx, reservation_detail in enumerate(reservationDetail):
            reservation_detail_obj = ReservationDetail()

            reservation_detail_obj.category_id = reservation_detail.category_id
            reservation_detail_obj.name_product = reservation_detail.name_product
            reservation_detail_obj.product_description = reservation_detail.product_description
            reservation_detail_obj.product_amount = reservation_detail.product_amount
            reservation_detail_obj.product_quantity = reservation_detail.product_quantity
            total_price += (reservation_detail.product_quantity * reservation_detail.product_amount)

            if idx == 0:
                reservations_detail_response.name = reservation_detail.name
                reservations_detail_response.last_name = reservation_detail.last_name
                reservations_detail_response.people = reservation_detail.people
                reservations_detail_response.street = reservation_detail.street
                reservations_detail_response.street_number = reservation_detail.street_number
                reservations_detail_response.state = reservation_detail.state
                reservations_detail_response.city = reservation_detail.city
                reservations_detail_response.country = reservation_detail.country
                reservations_detail_response.preference = reservation_detail.preference
                reservations_detail_response.reservation_date = reservation_detail.reservation_date
                reservations_detail_response.reservation_week_day = reservation_detail.reservation_date.strftime("%A")
                reservations_detail_response.hour = reservation_detail.hour

            reservation_detail_list.append(reservation_detail_obj)
        reservations_detail_response.total_price = total_price
        reservations_detail_response.reservation_detail = reservation_detail_list

        return reservations_detail_response
