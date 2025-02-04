import statistics


def calculate_salary(lower_limit, upper_limit):
    if lower_limit and upper_limit:
        average_salary = statistics.mean([int(lower_limit),
                                          int(upper_limit)])
    elif lower_limit and not upper_limit:
        average_salary = int(lower_limit)*1.2
    elif upper_limit and not lower_limit:
        average_salary = int(upper_limit)*0.8
    elif not lower_limit and not upper_limit:
        average_salary = None
    return average_salary
