import statistics
import requests


from itertools import count
from functions import calculate_salary


def process_vacancies_sj(vacancies):
    salary_stats = []
    for vacancy in vacancies:
        if vacancy['currency'] == 'rub':
            lower_limit = int(vacancy['payment_from'])
            upper_limit = int(vacancy['payment_to'])
            average_salary = calculate_salary(lower_limit, upper_limit)
            if average_salary:
                salary_stats.append(average_salary)
        return salary_stats


def search_vacancies_sj(secret_key, date_from, languages):
    table_data = [['Language', 'Total', 'Processed', 'Salary']]
    for language in languages:
        language_vacancies, vacancies_number = paginate_sj(language, date_from, secret_key)
        clear_average_salaries = process_vacancies_sj(language_vacancies)
        if clear_average_salaries:
            average_salary = int(statistics.mean(clear_average_salaries))
            number_processed = len(clear_average_salaries)
        else:
            average_salary = None
            number_processed = 0
        table_data.append([language, vacancies_number,
                           number_processed, average_salary])
    return table_data


def paginate_sj(language, date_from, secret_key):
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
        if page_payload['more'] is False:
            break
    return language_vacancies, vacancies_number
