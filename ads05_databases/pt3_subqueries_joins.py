# Part 3: Subqueries & Joins


def top_postcodes_for_chain_stores():
    """
    From the businesses table, select the top 10 most popular postal_code.
    They should be filtered to only count the restaurants owned by people/entities that own 5 or more restaurants.
    The result should:
    * return a row (postal_code, frequency) for each 10 selection
    * sort by descending order to get the most relevant zip codes
    :return: a string representing the SQL query
    :rtype: str
    """
    result = 'SELECT postal_code, COUNT(postal_code) as count FROM businesses as b\
         WHERE b.owner_name in\
              (SELECT owner_name FROM businesses GROUP BY owner_name\
                 HAVING COUNT(owner_name) > 4)\
        GROUP BY postal_code ORDER BY count DESC LIMIT 10'
    return result


def inspection_scores_in_94103():
    """
    First let's get an idea about the inspection score our competition has.
    Based on multiple inspections, find out the minimum Score (as "min_score"),
    average Score (as "avg_score") and maximum Score (as "max_score") for all restaurant in post code "94103".
    The average score should be rounded to one decimal.
    :return: a string representing the SQL query
    :rtype: str
    """
    result = 'SELECT\
                MIN(Score) as "min_score",\
                ROUND(AVG(Score),1) as "avg_score",\
                MAX(Score) as "max_score"\
            FROM (\
                SELECT * FROM businesses as b\
                INNER JOIN inspections as ins ON b.business_id = ins.business_id)\
            WHERE (postal_code == "94103") & (Score IS NOT NULL)'
    return result


def risk_categories_in_94103():
    """
    Now lets get more serious, and look at how many times restaurants with postal code 94103
    (that's Market street) has committed health violations and group them based on their risk category.
    The output should be (risk_category, count as frequency) and sorted in descending order by frequency
    :return: a string representing the SQL query
    :rtype: str
    """
    result = 'SELECT risk_category, count(risk_category) as count\
              FROM (\
                SELECT * FROM businesses as b\
                INNER JOIN violations as v ON b.business_id = v.business_id)\
                WHERE (postal_code == "94103")\
            GROUP BY risk_category\
            ORDER BY count DESC'
    return result
