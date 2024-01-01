from django import template
import math
register = template.Library()

@register.simple_tag
def cal_sell_price(price,discount):
    if discount is None or discount is 0:
        return price
    sellprice = price
    sellprice = price - (price * discount/100)
    return math.floor(sellprice)

@register.simple_tag
def progress_bar(total_quantity , Availability):
    return total_quantity - Availability
