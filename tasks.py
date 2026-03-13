def process_order(*args, **kwargs):
    total = 0
    for price in args:
        total += price
    discount = kwargs.get("discount", 0)
    delivery = kwargs.get("delivery", 5)
    vip = kwargs.get("vip", False)
    if vip:
        discount = discount * 2
    discount_price = total - (total * discount / 100)
    if discount_price > 100:
        delivery = 0
    final_price = discount_price + delivery
    return final_price
