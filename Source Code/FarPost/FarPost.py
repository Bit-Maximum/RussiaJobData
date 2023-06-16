from selenium import webdriver
import time
import json
from bs4 import BeautifulSoup

from datetime import datetime

# Время выполнения программы: ~1 час
def connect_driver():
    # Путь к драйверу Chrome
    driver_path = 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path=driver_path)
    return driver


def get_url_list():
    urls = ["https://www.farpost.ru/arsenev/rabota/vacansii/",
            "https://www.farpost.ru/artem/rabota/vacansii/",
            "https://www.farpost.ru/bolshoi-kamen/rabota/vacansii/",
            "https://www.farpost.ru/vladivostok/rabota/vacansii/",
            "https://www.farpost.ru/dalnegorsk/rabota/vacansii/",
            "https://www.farpost.ru/lesozavodsk/rabota/vacansii/",
            "https://www.farpost.ru/nakhodka/rabota/vacansii/",
            "https://www.farpost.ru/partizansk/rabota/vacansii/",
            "https://www.farpost.ru/spassk-dalnii/rabota/vacansii/",
            "https://www.farpost.ru/ussuriisk/rabota/vacansii/"]
    return urls


def month_int_to_str(month_int):
    month = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
        7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }
    return month.get(month_int)


def scroll_to_bottom(driver):  # Функция для прокручивания страницы до конца
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Ожидаем некоторое время для загрузки данных
        time.sleep(3)

        # Проверяем, достигнут ли конец страницы
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return


def get_html(driver):  # Функция для получения HTML-кода всей страницы
    scroll_to_bottom(driver)
    html_code = driver.page_source

    # Закрываем браузер
    driver.quit()
    return html_code


def process_data(html_code):
    current_month = datetime.now().month
    current_day = datetime.now().day
    domen = 'https://www.farpost.ru'
    soup = BeautifulSoup(html_code, 'html.parser')

    all_info = soup.find_all(class_="descriptionCell bull-item-content__cell bull-item-content__description-cell js-description-block")
    city_vacancies = []

    for item in all_info:
        title = item.find(class_='bulletinLink bull-item__self-link auto-shy').text
        try:
            salary = item.find(class_='price-block__price').text.replace("\xa0", "").replace("–", "-")
        except:
            salary = ""

        vacancy_url = domen + item.find(class_='bull-item-content__subject-container').find('a').get('href')
        try:
            date = item.find(class_='date').text
            if "вчера" in date:
                if current_day == 1:  # Костыль 
                    current_day
                date = date.replace("вчера", "12 июня")
            elif "сегодня" in date:
                date = date.replace("сегодня", f"{current_day} {month_int_to_str(current_month)}")
            date_parts = date.split(' в ')
            date = date_parts[0]
        except:
            date = "13 июня"

        try:
            place = item.find(class_='bull-delivery__city').text
        except:
            place = "Владивосток"

        try:
            corporation = item.find(class_='bull-item__annotation-row').text
        except:
            corporation = "Не указана"

        city_vacancies.append(
            {
                'Профессия': title,
                'Зарплата': salary,
                'Город': place,
                'Организация': corporation,
                'Ссылка': vacancy_url,
                'Дата': date
            }
        )

    with open('all_vacansii_list_vl.json', 'w', encoding="utf-8") as file:
        json.dump(city_vacancies, file, indent=4, ensure_ascii=False)


def get_farpost_data():
    urls = get_url_list()

    for url in urls:
        driver = connect_driver()
        driver.get(url)

        # Ожидаем загрузку страницы
        time.sleep(1)
        driver.maximize_window()

        html_code = get_html(driver)

    return df


def run_farpost():
    driver = connect_driver()
    return -1






def main():
    # get_data('https://www.farpost.ru/vladivostok/rabota/vacansii/')
    process_data()

# Вызываем функцию main для запуска скрипта
main()