import statistics


def count_average_salary(salary_stats):
    if salary_stats:
        counted_average_salary = int(statistics.mean(salary_stats))
    else:
        counted_average_salary = None
    return counted_average_salary


def process_language(language, vacancies, table_data, processor):
    salary_stats = []
    language_count = len(language)
    salary_stats, language_count = processor(vacancies, language,
                                             salary_stats, language_count)
    average_salary = count_average_salary(salary_stats)
    table_data.append([language, language_count,
                       len(salary_stats), average_salary])
    return table_data


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


def make_clear(list):
    result = [x for x in list if x is not None]
    return result
