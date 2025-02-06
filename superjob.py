import statistics
import requests


from itertools import count
from functions import calculate_salary


def process_vacancies_sj(vacancies):
    salaries = []
    for vacancy in vacancies:
        if vacancy['currency'] != 'rub':
            continue
        lower_limit = int(vacancy['payment_from'])
        upper_limit = int(vacancy['payment_to'])
        average_salary = calculate_salary(lower_limit, upper_limit)
        if not average_salary:
            continue
        salaries.append(average_salary)
    salary, number_processed = None, None
    if salaries:
        salary = int(statistics.mean(salaries))
        number_processed = len(salaries)
    return salary, number_processed


def get_vacancies_sj(language, date_from, secret_key):
    language_vacancies = []
    for page in count(0):
        url = "https://api.superjob.ru/2.0/vacancies/"
        headers = {'X-Api-App-Id': secret_key}
        payload = {'town': 'Москва',
                   'date_published_from': date_from,
                   'keyword': f'программист {language}',
                   'page': page,
                   'count': 100}
        page_response = requests.get(url, headers=headers, params=payload)
        page_response.raise_for_status()
        page_payload = page_response.json()
        page_vacancies = page_payload['objects']
        vacancies_number = page_payload['total']
        language_vacancies.extend(page_vacancies)
        if not page_payload['more']:
            break
    return language_vacancies, vacancies_number
