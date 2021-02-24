"""
ORDER AND CART MANAGEMENT

Orders are sets of items ordered by a customer
An ordered item has four components:
 - a name
 - a quantity (the number of such items bought)
 - a unit price (in pence)
 - a unit weight (in pounds)
Those are represented by a tuple.

NOTE: You can safely assume that all orders have all the required fields
(name, quantity, unit-price and unit-weight) so no validation needs to be made.

DO NOT MODIFY CONSTANTS
"""

ORDER_SAMPLE_1 = {("lamp", 2, 2399, 2), ("chair", 4, 3199, 10), ("table", 1, 5599, 85)}
ORDER_SAMPLE_2 = {("sofa", 1, 18399, 140), ("bookshelf", 2, 4799, 40)}

CATALOGUE = {("table", 9999, 20), ("chair", 2999, 5), ("lamp", 1999, 10)}


def delivery_charges(order):
    """
    Compute the delivery charges for an order. The company charges a flat £50
    fee plus £20 for each 100lbs (additional weight under 100lbs is ignored).

    E.g., delivery_charges({("desk", 1, 11999, 160)}) is 7000 (pence)
    E.g., delivery_charges({("desk", 2, 11999, 160)}) is 11000 (pence)
    E.g., delivery_charges({("lamp", 1, 2399, 2)}) is 5000 (pence)
    E.g., delivery_charges({("lamp", 50, 2399, 2)}) is 7000 (pence)

    :param order: order to process. See samples for examples.
    :return: delivery fee in pence
    :rtype: float | int
    """
    order_weight = sum([(x[1] * x[-1]) for x in order])

    order_total = 50
    while order_weight >= 100:
        order_weight -= 100
        order_total += 20
    return order_total * 100  # total from pounds to pence


def total_charge(order):
    """
    Compute the total charge for an order. It includes:
        - total price of items,
        - VAT (20% of the price of items),
        - delivery fee

    NOTE: in this computation, VAT is not applied to the delivery

    E.g., total_charge({("desk", 2, 11999, 160)}) is 39797 (pence)
    E.g., total_charge({("lamp", 50, 2399, 2)}) is 150940 (pence)

    Hint: Look up the built-in Python function round().

    :param order: order to process. See samples.
    :return: total price, in pence, rounded to the nearest penny.
    :rtype: float | int
    """

    tot_price = (sum([x[2] * x[1] for x in order]))
    tot_price += tot_price * 0.2 + delivery_charges(order)
    return int(round(tot_price, 0))


def add_item_to_order(name, quantity, order):
    """
    When a customer adds items to their basket, you need to update their order.

    The customer provides some of the details (the name of the item and
    the quantity they want). The rest (price and weight) needs to be looked up in
    the CATALOGUE provided above.

    NOTE: you must return a new order as a set and leave the argument unmodified.

    NOTE: if the order already contains some of the items, you must update the
    quantity field for that item; otherwise, you must add a new entry in the
    order

    NOTE: if the item cannot be found in the catalogue, the function should raise
    a KeyError.

    E.g., add_item_to_order("table", 1, {("table", 1, 9999, 20)}) is
        {("table", 2, 9999, 20)}
    E.g., add_item_to_order("chair", 1, {("table", 1, 9999, 20)}) is
        {("table", 1, 9999, 20), ("chair", 1, 2999, 5)}

    :param name: name of the item to add
    :param quantity: number of items to add
    :param order: previous order
    :return: a new order with the added items. If the item is unknown, raise a KeyError
    :rtype: set
    """

    update = []
    updated_order = list(map(list, order))
    search_input = find_item(name, updated_order)
    search_catalougue = find_item(name, CATALOGUE)
    if search_input:
        search_input[1] += quantity
    elif search_catalougue:
        update.append((name, quantity, search_catalougue[-2], search_catalougue[-1]))
    else:
        raise KeyError
    for entry in updated_order:
        if entry:
            update.append(entry)
    return set(map(tuple, update))


def find_item(name, list_to_search):
    if len(list_to_search) > 0:
        for x in list_to_search:
            if x[0] == name:
                return x
        print('Not found in catalogue')
