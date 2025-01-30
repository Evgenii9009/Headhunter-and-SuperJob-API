import statistics
import requests
from itertools import count
from functions import count_statistics


def process_salaries(clear_salary_stats):
    average_salaries = []
    for salary in clear_salary_stats:
        currency = salary['currency']
        first_border = salary['from']
        second_border = salary['to']
        if currency == 'RUR' and first_border and second_border:
            average_salary = statistics.mean([int(first_border),
                                              int(second_border)])
            average_salaries.append(average_salary)
    return average_salaries


def make_clear(list):
    result = [x for x in list if x is not None]
    return result


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
    count_statistics(all_vacancies,
                     processor=process_vacancies_hh,
                     title='HeadHunter')
