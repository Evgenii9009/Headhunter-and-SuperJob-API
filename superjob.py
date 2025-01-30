import statistics
import requests


from itertools import count
from functions import count_statistics


def process_vacancies_sj(vacancies, language, salary_stats, language_count):
    for vacancy in vacancies:
        if language in vacancy['profession']:
            language_count = language_count+1
            if vacancy['currency'] == 'rub':
                lower_limit = int(vacancy['payment_from'])
                upper_limit = int(vacancy['payment_to'])
                limits_sum = lower_limit+upper_limit
                if limits_sum:
                    average_salary = statistics.mean([limits_sum, 0])
                    salary_stats.append(average_salary)
    return salary_stats, language_count


def sj_searcher(date_from, secret_key):
    all_vacancies = []
    for page in count(0):
        url = "https://api.superjob.ru/2.0/vacancies/"
        headers = {'X-Api-App-Id': secret_key}
        payload = {'town': 'Москва',
                   'date_published_from': date_from,
                   'keyword': 'Программист',
                   'page': page,
                   'count': 100}
        page_response = requests.get(url, headers=headers, params=payload)
        page_response.raise_for_status()
        page_objects = page_response.json()['objects']
        all_vacancies.extend(page_objects)
        if page == 4:
            break
    count_statistics(all_vacancies,
                     processor=process_vacancies_sj,
                     title='HeadHunter')
