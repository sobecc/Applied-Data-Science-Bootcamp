def minimum_profitable_volume(sell_price, fixed_cost, cost_per_unit):
    """
    For this exercise, you will need to implement a function that
    computes the minimum number of units that need to be manufactured by a factory
    for their process to be profitable.

    We assume that every unit manufactured is sold at the sell_price.
    You will need to take into account the fixed_cost, which is a constant cost
    associated with manufactoring as well as the cost_per_unit that we have to pay for
    each unit manufactured.

    Your goal is to find how many units need to be built and sold
    in order for the total cost to be entirely covered by sales.

    E.g., minimum_profitable_volume(1020, 1000, 20) is 1
    E.g., minimum_profitable_volume(1019, 1000, 20) is 2
    E.g., minimum_profitable_volume(600, 1000, 20) is 2
    E.g., minimum_profitable_volume(30, 1000, 20) is 100
    E.g., minimum_profitable_volume(21, 1000, 20) is 1000

    Note: It isn't sustainable for the factory to sell a unit in a lower price than
    its manufacturing cost as it wouldn't make any profit. If that is the case and
    you cannot be profitable, return None.

    :param sell_price: price each unit is sold at
    :return: number of units that need to be made and sold
    :rtype: float | int
    """
    count = 0
    income = - fixed_cost
    make_sell_diff = sell_price - cost_per_unit
    while income < 0:
        count += 1
        income = income + make_sell_diff
    return count
