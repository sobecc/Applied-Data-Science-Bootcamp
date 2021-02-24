import re
from datetime import datetime as dt
from pyspark import SparkContext
sc = SparkContext.getOrCreate()


def count_elements_in_dataset(dataset):
    """
    Given a dataset loaded on Spark, return the
    number of elements.
    :param dataset: dataset loaded in Spark context
    :type dataset: a Spark RDD
    :return: number of elements in the RDD
    """
    return dataset.count()


def get_first_element(dataset):
    """
    Given a dataset loaded on Spark, return the
    first element
    :param dataset: dataset loaded in Spark context
    :type dataset: a Spark RDD
    :return: the first element of the RDD
    """
    for line in dataset.take(1):
        result = line

    return result


def get_all_attributes(dataset):
    """
    Each element is a dictionary of attributes and their values for a post.
    Can you find the set of all attributes used throughout the RDD?
    The function dictionary.keys() gives you the list of attributes of a dictionary.
    :param dataset: dataset loaded in Spark context
    :type dataset: a Spark RDD
    :return: all unique attributes collected in a list
    """
    attributes = []
    for line in dataset.take(50):
        for key in line.keys():
            if key not in attributes:
                attributes.append(key)
    return attributes


def get_attr(line):
    if not line:
        return 'Null'
    return ' '.join(line.keys())


def get_elements_w_same_attributes(dataset):
    """
    We see that there are more attributes than just the one used in the first element.
    This function should return all elements that have the same attributes
    as the first element.

    :param dataset: dataset loaded in Spark context
    :type dataset: a Spark RDD
    :return: an RDD containing only elements with same attributes as the
    first element
    """
    first_attr = get_attr(dataset.take(1)[0])
    same_attr_rdd = dataset.filter(lambda line: first_attr == get_attr(line))
    return same_attr_rdd


def get_min_max_timestamps(dataset):
    """
    Find the minimum and maximum timestamp in the dataset
    :param dataset: dataset loaded in Spark context
    :type dataset: a Spark RDD
    :return: min and max timestamp in a tuple object
    :rtype: tuple
    """
    stamps = dataset.map(lambda line: line['created_at_i'])
    min_time = stamps.min()
    max_time = stamps.max()
    return (dt.utcfromtimestamp(min_time), dt.utcfromtimestamp(max_time))


def get_bucket(rec, min_timestamp, max_timestamp):
    interval = (max_timestamp - min_timestamp + 1) / 200.0
    return int((rec['created_at_i'] - min_timestamp)/interval)


def get_number_of_posts_per_bucket(dataset, min_time, max_time):
    """
    Using the `get_bucket` function defined in the notebook (redefine it in this file), this function should return a
    new RDD that contains the number of elements that fall within each bucket.
    :param dataset: dataset loaded in Spark context
    :type dataset: a Spark RDD
    :param min_time: Minimum time to consider for buckets (datetime format)
    :param max_time: Maximum time to consider for buckets (datetime format)
    :return: an RDD with number of elements per bucket
    """
    all_buckets = dataset.map(lambda line: get_bucket(line, dt.timestamp(min_time), dt.timestamp(max_time)))
    stamp_count = all_buckets.map(lambda stamp: (stamp, 1))
    buckets_rdd = stamp_count.reduceByKey(lambda c1, c2: c1 + c2)

    return buckets_rdd.sortBy(lambda bin: bin[0])


def get_number_of_posts_per_hour(dataset):
    """
    Using the `get_hour` function defined in the notebook (redefine it in this file), this function should return a
    new RDD that contains the number of elements per hour.
    :param dataset: dataset loaded in Spark context
    :type dataset: a Spark RDD
    :return: an RDD with number of elements per hour
    """
    all_hour = dataset.map(lambda line: dt.utcfromtimestamp(line['created_at_i']))
    hour_count = all_hour.map(lambda stamp: (stamp.hour, 1))
    hour_rdd = hour_count.reduceByKey(lambda c1, c2: c1 + c2)

    return hour_rdd


def get_score_per_hour(dataset):
    """
    The number of points scored by a post is under the attribute `points`.
    Use it to compute the average score received by submissions for each hour.
    :param dataset: dataset loaded in Spark context
    :type dataset: a Spark RDD
    :return: an RDD with average score per hour
    """
    points_hour = dataset.map(lambda line: (dt.utcfromtimestamp(line['created_at_i']).hour, (line['points'], 1)))
    result = points_hour\
        .reduceByKey(lambda t1, t2: (t1[0] + t2[0], t1[1] + t2[1]))\
        .map(lambda pair: (pair[0], pair[1][0]/pair[1][1]))

    return result


def get_points(line):
    if line['points'] >= 200:
        return 1
    return 0


def get_proportion_of_scores(dataset):
    """
    It may be more useful to look at sucessful posts that get over 200 points.
    Find the proportion of posts that get above 200 points per hour.
    This will be the number of posts with points > 200 divided by the total number of posts at this hour.
    :param dataset: dataset loaded in Spark context
    :type dataset: a Spark RDD
    :return: an RDD with the proportion of scores over 200 per hour
    """
    result = dataset\
        .map(lambda line: (dt.utcfromtimestamp(line['created_at_i']).hour, (get_points(line), 1)))\
        .reduceByKey(lambda t1, t2: (t1[0] + t2[0], t1[1] + t2[1]))\
        .map(lambda pair: (pair[0], pair[1][0]/pair[1][1]))

    return result


def get_title_l(line):
    if 'title' in line:
        return len(re.compile("\\w+").findall(line['title']))
    return 0


def get_proportion_of_success(dataset):
    """
    Using the `get_words` function defined in the notebook to count the
    number of words in the title of each post, look at the proportion
    of successful posts for each title length.

    Note: If an entry in the dataset does not have a title, it should
    be counted as a length of 0.

    :param dataset: dataset loaded in Spark context
    :type dataset: a Spark RDD
    :return: an RDD with the proportion of successful post per title length
    """
    result = dataset\
        .map(lambda line: (get_title_l(line), (get_points(line), 1)))\
        .reduceByKey(lambda t1, t2: (t1[0] + t2[0], t1[1] + t2[1]))\
        .map(lambda pair: (pair[0], pair[1][0]/pair[1][1]))

    return result


def get_title_length_distribution(dataset):
    """
    Count for each title length the number of submissions with that length.

    Note: If an entry in the dataset does not have a title, it should
    be counted as a length of 0.

    :param dataset: dataset loaded in Spark context
    :type dataset: a Spark RDD
    :return: an RDD with the number of submissions per title length
    """
    result = dataset.map(lambda line: (get_title_l(line), 1)).reduceByKey(lambda l1, l2: l1+l2)

    return result
