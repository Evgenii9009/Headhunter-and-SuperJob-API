import statistics
from terminaltables import DoubleTable


def count_statistics(vacancies, **kwargs):
    processor = kwargs['processor']
    languages = ['JavaScript', 'Java',
                 'Python', 'Ruby',
                 'PHP', 'C++',
                 'C#', 'C',
                 'Go', 'Shell']
    title = kwargs['title']
    table_data = [['Language', 'Total', 'Processed', 'Salary']]
    global_stats = dict()
    for language in languages:
        language_count = 0
        salary_stats = []
        salary_stats, language_count = processor(vacancies, language,
                                                 salary_stats, language_count)
        average_salary = count_average_salary(salary_stats)
        table_data.append([language, language_count,
                           len(salary_stats), average_salary])
    table_instance = DoubleTable(table_data, title)
    print(table_instance.table)
    return global_stats


def count_average_salary(salary_stats):
    if salary_stats:
        counted_average_salary = int(statistics.mean(salary_stats))
    else:
        counted_average_salary = None
    return counted_average_salary
