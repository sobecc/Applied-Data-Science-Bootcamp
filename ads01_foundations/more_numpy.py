"""Some exercises that can be done with numpy (but you don't have to)"""
import numpy as np


def all_unique_chars(string):
    """
    Write a function to determine if a string is only made of unique
    characters and returns True if that's the case, False otherwise.
    Upper case and lower case should be considered as the same character.

    Example:
    "qwr#!" --> True, "q Qdf" --> False

    :param string: input string
    :type string:  string
    :return:      true or false if string is made of unique characters
    :rtype:        bool
    """
    string = string.lower()
    return len(set(string)) == len(string)


def find_element(sq_mat, val):
    """
    Write a function that takes a square matrix of integers and returns a set of all valid
    positions (i,j) of a value. Each position should be returned as a tuple of two
    integers.

    The matrix is structured in the following way:
    - each row has strictly decreasing values with the column index increasing
    - each column has strictly decreasing values with the row index increasing
    The following matrix is an example:

    Example 1 :
    mat = [ [10, 7, 5],
            [ 9, 4, 2],
            [ 5, 2, 1] ]
    find_element(mat, 4) --> {(1, 1)}

    Example 2 :
    mat = [ [10, 7, 5],
            [ 9, 4, 2],
            [ 5, 2, 1] ]
    find_element(mat, 5) --> {(0, 2), (2, 0)}

    The function should raise an exception ValueError if the value isn't found.

    :param sq_mat: the square input matrix with decreasing rows and columns
    :type sq_mat:  numpy.array of int
    :param val:    the value to be found in the matrix
    :type val:     int
    :return:       all positions of the value in the matrix
    :rtype:        set of tuple of int
    :raise ValueError:
    """
    indexes = np.argwhere(sq_mat == val)
    print(indexes)
    print(indexes.any())
    if indexes.size != 0:
        return set(map(tuple, indexes))
    raise ValueError


def filter_matrix(mat):
    """
    Write a function that takes an n x p matrix of integers and sets the rows
    and columns of every zero-entry to zero.

    Example:
    [ [1, 2, 3, 1],        [ [0, 2, 0, 1],
      [5, 2, 0, 2],   -->    [0, 0, 0, 0],
      [0, 1, 3, 3] ]         [0, 0, 0, 0] ]

    :param mat: input matrix
    :type mat:  numpy.array of int
    :return:   a matrix where rows and columns of zero entries in mat are zero
    :rtype:    numpy.array
    """
    rows = len(mat)
    cols = len(mat[0])
    res_mat = np.zeros((rows, cols))
    for row in range(rows):
        if mat[row].all(0):
            for col in range(cols):
                if mat[:, col].all(0):
                    res_mat[row, col] = mat[row, col]
    return res_mat


def largest_sum(intlist):
    """
    Write a function that takes in a list of integers,
    finds the sublist of contiguous values with at least one
    element that has the largest sum and returns the sum.
    If the list is empty, 0 should be returned.

    Example:
    [-1, 2, 7, -3] --> the sublist with larger sum is [2, 7], the sum is 9.

    :param intlist: input list of integers
    :type intlist:  list of int
    :return:       the largest sum
    :rtype:         int
    """
    current_sum = 0
    if not intlist:
        return current_sum
    max_sum = intlist[0]
    for _, x in enumerate(intlist):
        current_sum += x
        if x > max_sum:
            max_sum = x
        if current_sum > max_sum:
            max_sum = current_sum
        elif current_sum < 0:
            current_sum = 0
    return max_sum
