import requests
import statistics

from itertools import count
from terminaltables import DoubleTable
from functions import calculate_salary, make_clear


def process_salaries(clear_salary_stats):
    average_salaries = []
    for salary in clear_salary_stats:
        average_salary = count_average_salary(salary)
        average_salaries.append(average_salary)
    return average_salaries


def process_vacancies_hh(vacancies):
    salary_stats = []
    for vacancy in vacancies:
        salary_stats.append(vacancy['salary'])
    clear_salary_stats = make_clear(salary_stats)
    average_salaries = process_salaries(clear_salary_stats)
    clear_average_salaries = make_clear(average_salaries)
    return clear_average_salaries


def search_vacancies_hh(date_from):
    title = 'HeadHunter'
    table_data = [['Language', 'Total', 'Processed', 'Salary']]
    languages = ['JavaScript', 'Java',
                 'Python', 'Ruby',
                 'PHP', 'C++',
                 'C#', 'C',
                 'Go', 'Shell']
    download_vacancies_hh(languages, date_from, table_data)
    table_instance = DoubleTable(table_data, title)
    print(table_instance.table)


def count_average_salary(salary):
    currency = salary['currency']
    lower_limit = salary['from']
    upper_limit = salary['to']
    if currency == 'RUR':
        average_salary = calculate_salary(lower_limit, upper_limit)
        return average_salary


def download_vacancies_hh(languages, date_from, table_data):
    for language in languages:
        language_vacancies = paginate_hh(language, date_from)
        clear_average_salaries = process_vacancies_hh(language_vacancies)
        average_salary = statistics.mean(clear_average_salaries)
        table_data.append([language, len(language_vacancies),
                           len(clear_average_salaries), int(average_salary)])


def paginate_hh(language, date_from):
    moscow_city_code = 1
    vacancies_per_page = 100
    language_vacancies = []
    for page in count(0):
        url = 'https://api.hh.ru/vacancies'
        payload = {'text': f'программист {language}',
                   'area': moscow_city_code,
                   'date_from': date_from,
                   'page': page,
                   'per_page': vacancies_per_page}
        page_response = requests.get(url, params=payload)
        page_response.raise_for_status()
        page_payload = page_response.json()
        page_vacancies = page_payload['items']
        language_vacancies.extend(page_vacancies)
        if page == page_payload['pages']-1:
            break
    return language_vacancies
