"""
DATA PROCESSING

DO NOT MODIFY CONSTANTS
"""

PRICES_PER_HOUR_PER_DAY_SAMPLE = [
    [11300, 12000, 12100, 12100, 11800, 11100, 10300, 9400],  # Prices for business hours on Monday
    [10100, 10300, 10200, 10300, 10200, 10100, 10200, 10200],  # Prices for business hours on Tuesday
    [10600, 10700, 10100, 10000, 9800, 8400, 7500, 9000],  # Prices for business hours on Wednesday
    [9100, 9600, 10200, 10200, 10200, 10300, 10100, 10400],  # Prices for business hours on Thursday
    [10500, 10600, 13200, 10800, 10500, 10200, 9900, 9800]  # Prices for business hours on Friday
]


def length_check(prices):
    if len(prices) > 1:
        first_length = len(prices[0])
        for i in range(1, len(prices)):
            if len(prices[i]) != first_length:
                return False
    return True


def normalize_prices(prices):
    """
    This function takes a list of prices for a given commodity.

    The prices are given as a list of list of numbers. Each inner list corresponds
    to a day of the week, and each number corresponds to the price at a given
    hour of the day (limited to business hours only).

    See the example of PRICES_PER_HOUR_PER_DAY_SAMPLE above. Here we have a list
    containing five lists (so the data is for one week only), each inner list
    contains 8 numbers, for 8 hours in the day.

    This function should normalise all the prices such that the first value is
    worth 100 and the other are adjusted accordingly.

    E.g., normalize_prices([[1, 2], [3, 4]]) is [[100, 200], [300, 400]]
    E.g., normalize_prices([[200, 20], [30, 400]]) is [[100, 10], [15, 200]]

    NOTE: prices need to consist of lists of the same length meaning that no prices
    for given hours are missing and if they are, you must raise a ValueError.

    :param prices: list of list of prices
    :return: normalised list of list of prices where the first price is 100
    and the other prices are scaled accordingly
    :rtype: list≈
    """
    if length_check(prices) is False:
        raise ValueError

    normalized = []
    first_price = prices[0][0]
    for i in range(len(prices)):
        temp = [x/first_price * 100 for x in prices[i]]
        normalized.append(temp)
    return normalized


def flip_prices(prices):
    """
    This function returns a list of daily prices for each observed hour given
    a list of hourly prices for each observed day.

    E.g., flip_prices([[1, 2, 3], [4, 5, 6]]) is [[1, 4], [2, 5], [3, 6]]

    NOTE: prices need to consist of lists of the same length meaning that no prices
    for given hours are missing and if they are, you must raise a ValueError.

    :param prices: list (for days) of list (for hours) of prices
    :return: list (for hours) of list (for days) of prices
    :rtype: list
    """
    if length_check(prices) is False:
        raise ValueError

    return list(zip(*prices))
