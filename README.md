# Сравниваем вакансии программистов

Код предназначен для сравнения вакансий разработчиков на разных языках программирования с двух популярных ресурсов: HeadHunter и SuperJob.
Обрабатывается следующая информация:

-  Количество размещенных вакансий для языка программирования
-  Количество вакансий с указанными зарплатами
-  Средняя зарплата разработчиков для каждого языка

### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Запуск

Для работы вам необходимо зарегистрировать приложение на [API Superjob](https://api.superjob.ru/) и получить его ключ.
Данный ключ необходимо положить в переменную окружения `SUPERJOB_SECRET_KEY`

Запуск осуществляется командой 

```
python3 main.py
```
### Пример работы

![image](https://github.com/user-attachments/assets/e35813b8-a1a2-4662-aa92-847ef539df74)


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
