import datetime
import os


from headhunter import hh_searcher
from superjob import sj_searcher


def main():
    date_from = datetime.date.today() - datetime.timedelta(days=30)
    secret_key = os.getenv('SECRET_KEY')
    sj_searcher(date_from, secret_key)
    hh_searcher(date_from)


if __name__ == '__main__':
    main()
