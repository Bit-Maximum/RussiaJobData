import os
import datetime

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

import asyncio


# Время выполнения программы: ~1 час

SEC_WAIT_TO_SCROLL = 3
SEC_WAIT_TO_LOAD_PAGE = 1


def check_connection():
    print("Подключение к FarPost.ru: ", end="")
    url = 'https://www.farpost.ru/vladivostok/rabota/'
    response = requests.get(url=url)
    if response.status_code == 200:
        print("OK")
        return
    else:
        print("Ошибка соединения. Сервис FarPost.ru не доступен.")
        raise Exception


def connect_driver():
    # Запуск браузера в фоновом режиме
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


# Ссылки должны идти в том же порядке, что и список городов
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


# Города должны идти в том же порядке, что и список ссылок
def get_city_list():
    city = ["Арсеньев", "Артем",
            "Большой Камень", "Владивосток",
            "Дальнегорск", "Лесозаводск",
            "Находка", "Партизанск",
            "Спасск-Дальний", "Уссурийск"]
    return city


def month_int_to_str(month_int):
    month = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
        7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }
    return str(month.get(month_int))


def month_str_to_int(month_str):
    month = {
        "января": 1, "февраля": 2, "марта": 3, "апреля": 4, "мая": 5, "июня": 6,
        "июля": 7, "августа": 8, "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12
    }
    return month.get(month_str)


async def scroll_to_bottom(driver):  # Функция для прокручивания страницы до конца
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Ожидаем некоторое время для загрузки данных
        await asyncio.sleep(SEC_WAIT_TO_SCROLL)

        # Проверяем, достигнут ли конец страницы
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return


async def get_html(driver):  # Функция для получения HTML-кода всей страницы
    await scroll_to_bottom(driver)
    html_code = driver.page_source

    # Закрываем браузер
    driver.quit()
    return html_code


def process_data(html_code, city):
    domen = 'https://www.farpost.ru'
    soup = BeautifulSoup(html_code, 'html.parser')

    all_info = soup.find_all(
        class_="descriptionCell bull-item-content__cell bull-item-content__description-cell js-description-block"
    )
    city_vacancies = {
        "Профессия": [], "Зарплата": [], "Населённый пункт": [], "Наниматель": [],
        "Ссылка": [], "Дата публикации": [], "Дата сбора данных": []
    }

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
                yesterday = datetime.date.today() - datetime.timedelta(days=1)
                date = date.replace("вчера", f"{yesterday.day} {month_int_to_str(yesterday.month)}")
            elif "сегодня" in date:
                today_date = datetime.date.today()
                date = date.replace("сегодня", f"{today_date.day} {month_int_to_str(today_date.month)}")
            date_parts = date.split(' в ')
            date = date_parts[0]
        except:
            today_date = datetime.date.today()
            date = f"{today_date.day} {month_int_to_str(today_date.month)}"

        try:
            place = item.find(class_='bull-delivery__city').text
        except:
            place = city

        try:
            corporation = item.find(class_='bull-item__annotation-row').text
        except:
            corporation = "Не указана"

        city_vacancies["Профессия"].append(title)
        city_vacancies["Зарплата"].append(salary)
        city_vacancies["Населённый пункт"].append(place)
        city_vacancies["Наниматель"].append(corporation)
        city_vacancies["Ссылка"].append(vacancy_url)
        city_vacancies["Дата публикации"].append(date)
        city_vacancies["Дата сбора данных"] = datetime.date.today()

    return pd.DataFrame(city_vacancies)


async def get_farpost_data():
    print("FarPost: фильтрация собранных данных")
    urls = get_url_list()
    cities = get_city_list()
    dfs = []  # Список для DataFrame с каждого города
    for num, url in enumerate(urls):
        driver = connect_driver()
        driver.get(url)

        # Ожидаем загрузку страницы
        await asyncio.sleep(SEC_WAIT_TO_LOAD_PAGE)
        driver.maximize_window()
        city = cities[num]

        html_code = await get_html(driver)
        dfs.append(process_data(html_code, city))
        print(f"FarPost: данные собраны по {num + 1} из {len(urls)} городов")

    total_df = pd.concat(dfs, ignore_index=True)
    return total_df


def filter_data(df):
    # Получаем ID-вакансий
    df["Ссылка"] = df["Ссылка"].apply(lambda x: x.split('-')[-1])
    df["Ссылка"] = df["Ссылка"].apply(lambda x: x.rstrip('.html'))

    # Удаление дубликатов
    df = df.drop_duplicates(subset=["Ссылка"], keep="first", inplace=False)

    # Восстанавливаем недостающие столбцы
    df["Вакансия"] = df["Профессия"]
    df["Требуемый опыт работы"] = "Не указан"
    df["Зарплата до"] = df["Зарплата"]
    df["Вакантных мест"] = 1
    df["Источник"] = "FarPost"

    # Получаем значения атрибутов из "сырых" данных
    df["Зарплата до"] = df["Зарплата до"].apply(lambda x: x.split('-')[1] if '-' in x else "")
    df["Зарплата до"] = df["Зарплата до"].apply(lambda x: x.rstrip('₽') if '₽' in x else "")
    df["Зарплата"] = df["Зарплата"].apply(lambda x: x.rstrip('₽') if '₽' in x else "")
    df["Зарплата"] = df["Зарплата"].apply(lambda x: x.split('-')[0] if '-' in x else x)
    df["Зарплата"] = df["Зарплата"].apply(lambda x: x.strip('от ') if 'от ' in x else x)
    df["Наниматель"] = df["Наниматель"].apply(lambda x: x.split('. Ул')[0] if '. Ул' in x else x)
    df["Наниматель"] = df["Наниматель"].apply(lambda x: x.split('. Г')[0] if '. Г' in x else x)
    df["Наниматель"] = df["Наниматель"].apply(lambda x: x.split('. Бух')[0] if '. Бух' in x else x)
    df["Наниматель"] = df["Наниматель"].apply(lambda x: x.split('. Пер')[0] if '. Пер' in x else x)
    df["Наниматель"] = df["Наниматель"].apply(lambda x: x.split('. Пр')[0] if '. Пр' in x else x)

    # Форматируем даты
    df["Дата публикации"] = df["Дата публикации"].apply(lambda x: x.split())
    dates = df["Дата публикации"].tolist()
    current_year = int(datetime.date.today().year)
    filtered_dates = []
    for date in dates:
        month = month_str_to_int(date[1])
        day = int(date[0])
        filtered_dates.append(datetime.date(current_year, month, day))
    df["Дата публикации"] = filtered_dates

    # Меняем тип данных
    df["Дата публикации"] = df["Дата публикации"].astype("datetime64[ns]")
    df["Дата сбора данных"] = df["Дата сбора данных"].astype("datetime64[ns]")

    # Форматируем таблицу
    df.columns = ["Профессия", "Зарплата от", "Населённый пункт", "Наниматель", "ID",
                  "Дата публикации", "Дата сбора данных", "Вакансия",
                  "Требуемый опыт работы", "Зарплата до", "Вакантных мест", "Источник"]
    df = df[["Источник", "ID", "Профессия", "Вакансия", "Населённый пункт", "Требуемый опыт работы", "Зарплата от",
             "Зарплата до", "Дата публикации", "Дата сбора данных", "Наниматель", "Вакантных мест"]]
    return df


async def run_farpost():
    try:
        check_connection()
        print("FarPost: начинаем собирать данные")
        df = await get_farpost_data()
        df = filter_data(df)
        return df
    except Exception:
        print("FarPost: произошла ошибка. Сбор данных с источника остановлен.")


async def collect_to_excel():
    df_farpost = await run_farpost()
    today_date = datetime.date.today()
    path_to_export = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'FarPost',
                                  f"FarPost - {today_date}.xlsx")
    df_farpost.to_excel(path_to_export, sheet_name='Данные', index=False)


async def main():
    task = asyncio.create_task(collect_to_excel())
    await task


if __name__ == "__main__":
    asyncio.run(main())
