
import requests
import datetime
import statistics
import os
from terminaltables import DoubleTable
from itertools import count


def count_statistics(vacancies, **kwargs):
    processor = kwargs['processor']
    languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Shell']
    title = kwargs['title']
    table_data = [['Language', 'Total', 'Processed', 'Salary']]
    global_stats = dict()
    for language in languages:
        language_count = 0
        salary_stats = []
        salary_stats, language_count = processor(vacancies, language, salary_stats, language_count)
        average_salary = count_average_salary(salary_stats)
        table_data.append([language, language_count, len(salary_stats), average_salary])
    table_instance = DoubleTable(table_data, title)
    print(table_instance.table)
    return global_stats


def process_salaries(clear_salary_stats):
    average_salaries = []
    for salary in clear_salary_stats:
        currency = salary['currency']
        first_border = salary['from']
        second_border = salary['to']
        if currency == 'RUR' and first_border!=None and second_border !=None:
            average_salary = statistics.mean([int(first_border), int(second_border)])
            average_salaries.append(average_salary)
    return average_salaries


def make_clear(list):
    result = [x for x in list if x is not None]
    return result


def count_average_salary(salary_stats):
    if salary_stats:
        counted_average_salary = int(statistics.mean(salary_stats))
    else:
        counted_average_salary = None
    return counted_average_salary


def process_vacancies_sj(vacancies, language, salary_stats, language_count):
    for vacancy in vacancies:
        if language in vacancy['profession']:
            language_count = language_count+1
            if vacancy['currency']=='rub':
                lower_limit = int(vacancy['payment_from'])
                upper_limit = int(vacancy['payment_to'])
                limits_sum = lower_limit+upper_limit
                if limits_sum:
                    average_salary = statistics.mean([limits_sum, 0])
                    salary_stats.append(average_salary)
    return salary_stats, language_count


def process_vacancies_hh(vacancies, language, salary_stats, language_count):
    for vacancy in vacancies:
        if language in vacancy['name']:
            language_count = language_count+1
            salary_stats.append(vacancy['salary'])
    clear_salary_stats = make_clear(salary_stats)
    average_salaries = process_salaries(clear_salary_stats)
    clear_average_salaries = make_clear(average_salaries)
    return clear_average_salaries, language_count


def hh_searcher(date_from):
    all_vacancies = []
    for page in count(0):
        url = 'https://api.hh.ru/vacancies'
        payload = {'text': 'программист',
                    'area': 1,
                    'date_from': date_from,
                    'page': page,
                    'per_page': 100}
        page_response = requests.get(url, params=payload)
        page_response.raise_for_status()
        page_items = page_response.json()['items']
        all_vacancies.extend(page_items)
        if page == 19:
            break
    count_statistics(all_vacancies, processor=process_vacancies_hh, title='HeadHunter')


def sj_searcher(date_from):
    all_vacancies = []
    for page in count(0):
        url = "https://api.superjob.ru/2.0/vacancies/"
        secret_key = os.getenv('SECRET_KEY')
        headers = {'X-Api-App-Id': secret_key}
        payload = {'town': 'Москва',
                  'date_published_from': date_from,
                  'keyword': 'Java',
                  'page': page,
                  'count': 100}
        page_response = requests.get(url, headers=headers, params=payload)
        page_response.raise_for_status()
        page_objects = page_response.json()['objects']
        all_vacancies.extend(page_objects)
        if page == 4:
            break
    count_statistics(all_vacancies, processor=process_vacancies_sj, title='SuperJob')


def main():
    date_from = datetime.date.today() - datetime.timedelta(days=30)
    sj_searcher(date_from)
    hh_searcher(date_from)


if __name__=='__main__':
    main()