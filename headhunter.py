import requests
import statistics

from itertools import count
from functions import calculate_salary


def process_vacancies_hh(vacancies):
    average_salaries = []
    for vacancy in vacancies:
        if vacancy['salary'] and count_average_salary(vacancy['salary']):
            average_salaries.append(count_average_salary(vacancy['salary']))
    number_processed = len(average_salaries)
    average_salary = int(statistics.mean(average_salaries))
    return average_salary, number_processed


def count_average_salary(salary):
    currency = salary['currency']
    lower_limit = salary['from']
    upper_limit = salary['to']
    if currency == 'RUR':
        average_salary = calculate_salary(lower_limit, upper_limit)
        return average_salary


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
        vacancies_number = page_payload['found']
        language_vacancies.extend(page_vacancies)
        if page == page_payload['pages']-1:
            break
    return language_vacancies, vacancies_number
