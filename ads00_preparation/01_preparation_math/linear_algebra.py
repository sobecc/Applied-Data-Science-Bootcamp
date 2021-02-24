"""
This file contains a set of functions to practice your
linear algebra skills.

It needs to be completed using "vanilla" Python, without
help from any library.
"""


def gradient(w1, w2, x):
    """
    Given the following function f(x) = w1 * x1^2 + w2 * x2
    where x is a valid vector with coordinates [x1, x2]
    evaluate the gradient of the function at the point x

    :param w1: first coefficient
    :param w2: second coefficient
    :param x: a point represented by a valid tuple (x1, x2)
    :return: the two coordinates of gradient of f
    at point x
    :rtype: float, float
    """
    if len(x) == 2:
        return w1*2*x[0], w2
    raise ValueError


def metrics(u, v):
    """
    Given two vectors u and v, compute the following distances/norm between
    the two and return them.
    - l1 Distance (norm)
    - l2 Distance (norm)

    If the two vectors have different dimensions,
    you should raise a ValueError

    :param u: first vector (list)
    :param v: second vector (list)
    :return: l1 distance, l2 distance
    :rtype: float, float
    :raise ValueError:
    """
    _l1 = 0
    _l2 = 0
    if len(u) == len(v):
        for i, n in enumerate(u):
            value = n - v[i]
            _l1 = _l1 + abs(value)
            _l2 = _l2 + (value**2)
    else:
        raise ValueError
    return _l1, _l2**0.5


def list_mul(u, v):
    """
    Given two vectors, calculate and return the following quantities:
    - element-wise sum
    - element-wise product
    - dot product

    If the two vectors have different dimensions,
    you should raise a ValueError

    :param u: first vector (list)
    :param v: second vector (list)
    :return: the three quantities above
    :rtype: list, list, float
    :raise ValueError:
    """
    if len(u) == len(v):
        sum_vectors = [u[i] + v[i] for i in range(len(u))]
        product_vectors = [u[i] * v[i] for i in range(len(u))]
        dot_product_vectors = sum(product_vectors)
    else:
        raise ValueError
    return sum_vectors, product_vectors, dot_product_vectors


def matrix_mul(A, B):
    """
    Given two valid matrices A and B represented as a list of lists,
    implement a function to multiply them together (A * B). Your solution
    can either be a pure mathematical one or a more pythonic one where you
    make use of list comprehensions.

    For example:
    A = [[1, 2, 3],
         [4, 5, 6]]
    is a matrix with two rows and three columns.

    If the two matrices have incompatible dimensions or are not valid meaning that
    not all rows in the matrices have the same length you should raise a ValueError.

    :param A: first matrix (list of lists)
    :param B: second matrix (list of lists)
    :return: resulting matrix (list of lists)
    :rtype: list of lists
    :raise ValueError:
    """
    new_matrix = []

    dimensions_a = [len(a) for a in A]
    dimensions_b = [len(b) for b in B]

    if len(set(dimensions_a)) != 1 or len(set(dimensions_b)) != 1 or len(A[0]) != len(B):
        raise ValueError

    for row in A:
        new_row = [sum([i*j for (i, j) in zip(row, col)]) for col in zip(*B)]
        new_matrix.append(new_row)

    return new_matrix
