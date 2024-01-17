# from sh import lp
from escpos.printer import Network

from django.template.loader import render_to_string

from orders.models import Order, OrderItem

from django.conf import settings

def print_receipt(customer=False, **kwargs) -> None:

    printer_ip = settings.PRINTER_IP

    if customer:
        order = kwargs['order']

        order_items = order.items.all()
        table = order.table
        comment = order.comments
    else:
        order_items = kwargs['items']
        table = kwargs['table']
        comment = kwargs['comment']

    printer = Network(printer_ip)
    printer.charcode('CP866')

    printer.set(align="center")
    if customer:
        printer.text("Web-Motion LLC\n")
        printer.text("Turusbekova 109/3, Bishkek\n")
        printer.text("www.motion-webllc.com\n\n")

        printer.text(f"Стол: {table}\n\n")

    printer.set(align="left")
    total_price = 0
    for order_item in order_items:
        print(order_item)
        if customer:
            name = order_item.dish.name_ru
            price = order_item.dish.price
            quantity = order_item.quantity
        else:
            name = order_item['dish'].name_ru
            price = order_item['dish'].price
            quantity = order_item['quantity']

        total_price += int(price) * int(quantity)
        printer.text(f"{name}{' '*(35-len(name))}{quantity}x{int(price)}={int(quantity*price)}c.\n")

    printer.text('\n\n')
    if customer:
        printer.text(f'Общий счет: {total_price}')
    else:
        if comment != '-':
            printer.text(f"{comment}\n")

    print("PRINTING")
    printer.cut()