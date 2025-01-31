import datetime
import os


from headhunter import search_vacancies_hh
from superjob import search_vacancies_sj


def main():
    date_from = datetime.date.today() - datetime.timedelta(days=30)
    secret_key = os.getenv('SUPERJOB_SECRET_KEY')
    search_vacancies_hh(date_from)
    search_vacancies_sj(date_from, secret_key)


if __name__ == '__main__':
    main()
