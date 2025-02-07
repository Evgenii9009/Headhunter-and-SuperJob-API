import datetime
import os


from headhunter import get_vacancies_hh, process_vacancies_hh
from superjob import get_vacancies_sj, process_vacancies_sj
from functions import create_table


def main():
    languages = ['JavaScript', 'Java',
                 'Python', 'Ruby',
                 'PHP', 'C++',
                 'C#', 'C',
                 'Go', 'Shell']
    table_data_hh = [['Language', 'Total', 'Processed', 'Salary']]
    table_data_sj = [['Language', 'Total', 'Processed', 'Salary']]
    date_from = datetime.date.today() - datetime.timedelta(days=30)
    secret_key = os.getenv('SUPERJOB_SECRET_KEY')
    title_hh = 'HeadHunter'
    title_sj = 'SuperJob'

    for language in languages:
        vacancies, vacancies_number = get_vacancies_hh(language, date_from)
        salary, number_processed = process_vacancies_hh(vacancies)
        table_data_hh.append([language, vacancies_number,
                              number_processed, salary])
        vacancies, vacancies_number = get_vacancies_sj(language, date_from, secret_key)
        salary, number_processed = process_vacancies_sj(vacancies)
        table_data_sj.append([language, vacancies_number,
                              number_processed, salary])

    create_table(table_data_hh, title_hh)
    create_table(table_data_sj, title_sj)


if __name__ == '__main__':
    main()
