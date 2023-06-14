import requests
from selenium import webdriver
import time
import json
from bs4 import BeautifulSoup

# Путь к драйверу Chrome
driver_path = '/farpost/chromedriver/chromedriver.exe'

# Создание экземпляра драйвера
driver = webdriver.Chrome(executable_path=driver_path)

# Базовый URL страницы
base_url = 'https://www.farpost.ru/vladivostok/rabota/vacansii/'

# Открытие страницы
driver.get(base_url)
time.sleep(1)

# Максимизация окна браузера
driver.maximize_window()

# Функция для прокручивания страницы до конца
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Прокручиваем страницу до конца
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Ожидаем некоторое время для загрузки данных
        time.sleep(3)

        # Проверяем, достигнут ли конец страницы
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height

# # Функция для получения HTML-кода всей страницы
# def get_data(url):
#     # Скроллим страницу до конца
#     scroll_to_bottom()
#
#     # Получаем HTML-код страницы
#     html_code = driver.page_source
#
#     # Сохраняем HTML-код в файл
#     with open('farpost_html.html', 'w', encoding="utf-8") as file:
#         file.write(html_code)
#
#     # Закрываем браузер
#     driver.quit()

def process_data():
    with open('farpost_html.html', 'r', encoding='utf-8') as file:
        html_code = file.read()

    soup = BeautifulSoup(html_code, 'html.parser')

    all_info = soup.find_all(class_="descriptionCell bull-item-content__cell bull-item-content__description-cell js-description-block")

    all_vacansii_list11 = []

    for i in all_info:
        try:
            title = i.find(class_='bulletinLink bull-item__self-link auto-shy').text
        except:
            title = "Без названия"
        try:
            salary = i.find(class_='price-block__price').text.replace("\xa0", "").replace("–", "-")
        except:
            salary = "Не указана"
        try:
            url = 'https://www.farpost.ru' + i.find(
                class_='bull-item-content__subject-container').find('a').get('href')
        except:
            url = "Не указана"

        try:
            date = i.find(class_='date').text
            if "вчера" in date:
                date = date.replace("вчера", "12 июня")
            elif "сегодня"in date:
                date = date.replace("сегодня", "13 июня")
            date_parts = date.split(' в ')
            date = date_parts[0]
        except:
            date = "13 июня"

        try:
            place = i.find(class_='bull-delivery__city').text
        except:
            place = "Владивосток"

        try:
            corporation = i.find(class_='bull-item__annotation-row').text
        except:
            corporation = "Не указана"

        all_vacansii_list11.append(
            {
                'Профессия': title,
                'Зарплата': salary,
                'Город': place,
                'Организация': corporation,
                'Ссылка': url,
                'Дата': date
            }
        )

    with open('all_vacansii_list_vl.json', 'w', encoding="utf-8") as file:
        json.dump(all_vacansii_list11, file, indent=4, ensure_ascii=False)

def main():
    # get_data('https://www.farpost.ru/vladivostok/rabota/vacansii/')
    process_data()

# Вызываем функцию main для запуска скрипта
main()