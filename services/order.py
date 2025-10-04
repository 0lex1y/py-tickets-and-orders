from django.db.models import QuerySet

from db.models import Ticket, Order, User

from django.db import transaction


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None) -> dict:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=date)
        for ticket_dict in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket_dict["movie_session"],
                seat=ticket_dict["seat"],
                row=ticket_dict["row"],
            )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username is not None:
        orders = orders.filter(user__username=username)
    return orders
