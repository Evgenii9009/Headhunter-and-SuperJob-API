import statistics
import requests


from itertools import count
from functions import calculate_salary, make_clear
from terminaltables import DoubleTable


def process_vacancies_sj(vacancies):
    salary_stats = []
    for vacancy in vacancies:
        if vacancy['currency'] == 'rub':
            lower_limit = int(vacancy['payment_from'])
            upper_limit = int(vacancy['payment_to'])
            average_salary = calculate_salary(lower_limit, upper_limit)
            salary_stats.append(average_salary)
            clear_salary_stats = make_clear(salary_stats)
        return clear_salary_stats


def search_vacancies_sj(date_from, secret_key):
    title = 'Supejob'
    table_data = [['Language', 'Total', 'Processed', 'Salary']]
    languages = ['JavaScript', 'Java',
                 'Python', 'Ruby',
                 'PHP', 'C++',
                 'C#', 'C',
                 'Go', 'Shell']
    download_sj_vacancies(languages, secret_key, date_from, table_data)
    table_instance = DoubleTable(table_data, title)
    print(table_instance.table)


def download_sj_vacancies(languages, secret_key, date_from, table_data):
    for language in languages:
        language_vacancies = []
        language_vacancies = paginate_sj(language, date_from, language_vacancies, secret_key)
        clear_average_salaries = process_vacancies_sj(language_vacancies)
        if clear_average_salaries:
            average_salary = int(statistics.mean(clear_average_salaries))
            number_processed = len(clear_average_salaries)
        else:
            average_salary = None
            number_processed = 0
        table_data.append([language, len(language_vacancies),
                           number_processed, average_salary])


def paginate_sj(language, date_from, language_vacancies, secret_key):
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
        page_objects = page_response.json()['objects']
        language_vacancies.extend(page_objects)
        if page == 4:
            break
    return language_vacancies
