import datetime
import os


from headhunter import search_vacancies_hh
from superjob import search_vacancies_sj
from functions import create_table


def main():
    languages = ['JavaScript', 'Java',
                 'Python', 'Ruby',
                 'PHP', 'C++',
                 'C#', 'C',
                 'Go', 'Shell']
    date_from = datetime.date.today() - datetime.timedelta(days=30)
    secret_key = os.getenv('SUPERJOB_SECRET_KEY')

    table_data_hh = search_vacancies_hh(date_from, languages)
    title_hh = 'HeadHunter'
    create_table(table_data_hh, title_hh)

    table_data_sj = search_vacancies_sj(secret_key, date_from, languages)
    title_sj = 'SuperJob'
    create_table(table_data_sj, title_sj)


if __name__ == '__main__':
    main()
