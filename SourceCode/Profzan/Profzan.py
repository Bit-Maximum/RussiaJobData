import os
import datetime

from bs4 import BeautifulSoup
import pandas as pd
import requests

import asyncio
from aiohttp import ClientSession

# Для валидации URL-адреса
import urllib3


# Время исполнения программы: ~30 сек
def check_connection():
    print("Подключение к profzan.primorsky.ru: ", end="")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = 'https://profzan.primorsky.ru/vacancy/'
    response = requests.get(url=url, verify=False)
    if response.status_code == 200:
        print("OK")
        return
    else:
        print("Ошибка соединения. Сервис profzan.primorsky.ru не доступен.")
        raise Exception


async def get_html():
    items_on_page = 20000  # Должно быть больше суммарного числа объявлений на сайте

    async with ClientSession() as session:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url = 'https://profzan.primorsky.ru/vacancy/'
        params = {
            "SearchType": 1,
            "Region": 25,
            "Sort": 1,
            "PageSize": items_on_page,
            "Grid-page": 1
        }
        response = requests.get(url=url, params=params, verify=False)
        return response.text


async def get_profzan_data():
    html = await get_html()
    soup = BeautifulSoup(html, 'lxml')

    name = []
    salary = []
    area = []
    company = []
    date = []
    vacancies = []
    href = []

    main_table = soup.find_all('tr')

    for row in main_table:
        column = row.find_all('td')
        counter = 0
        for item in column:
            if item.text != '\n\n':
                counter += 1
                match counter:
                    case 1:
                        href.append(item.find_all('a')[0].attrs['href'])
                        name.append(item.text.replace("\n", ""))
                    case 2:
                        salary.append(item.text.replace("\n", ""))
                    case 3:
                        area.append(item.text.replace("\n", ""))
                    case 4:
                        company.append(item.text.replace("\n", ""))
                    case 5:
                        date.append(item.text.replace("\n", ""))
                    case 6:
                        vacancies.append(item.text.replace("\n", ""))

    total_df = pd.DataFrame({'Профессия': name,
                             'Зарплата': salary,
                             'Населённый пункт': area,
                             'Наниматель': company,
                             'Дата публикации': date,
                             'Вакантных мест': vacancies,
                             'Ссылка': href,
                             })

    total_df["Дата сбора данных"] = datetime.date.today()
    return total_df


def filter_data(df):
    # Удаление дубликатов
    df = df.drop_duplicates(subset=["Ссылка"])

    # Восстанавливаем недостающие столбцы
    df["Вакансия"] = df["Профессия"]
    df["Зарплата до"] = df["Зарплата"]
    df["Требуемый опыт работы"] = "Не указан"
    df["Источник"] = "Центр занятости Приморского края"

    # Получаем значения атрибутов из "сырых" данных
    df["Ссылка"] = df["Ссылка"].apply(lambda x: x.split('detail/')[1] if 'detail/' in x else x)
    df["Ссылка"] = df["Ссылка"].apply(lambda x: x.split('/?return')[0] if '/?return' in x else x)
    df["Населённый пункт"] = df["Населённый пункт"].apply(lambda x: x.split(' г ')[1] if ' г ' in x else x)
    df["Населённый пункт"] = df["Населённый пункт"].apply(lambda x: x.split(', ')[-1] if ', ' in x else x)
    df["Населённый пункт"] = df["Населённый пункт"].apply(lambda x: x.replace('с ', '') if 'с ' in x else x)
    df["Населённый пункт"] = df["Населённый пункт"].apply(lambda x: x.replace('пгт ', '') if 'пгт ' in x else x)
    df["Зарплата до"] = df["Зарплата до"].apply(lambda x: x.split('до')[1] if 'до' in x else "")
    df["Зарплата"] = df["Зарплата"].apply(lambda x: x.split('до')[0] if 'до' in x else x)
    df["Зарплата"] = df["Зарплата"].apply(lambda x: x.replace('от', '') if 'от' in x else x)

    # Меняем тип данных
    df["Вакантных мест"] = df["Вакантных мест"].astype("int64")
    df["Дата сбора данных"] = df["Дата сбора данных"].astype("datetime64[ns]")

    df["Дата публикации"] = df["Дата публикации"].apply(lambda x: x.split('.') if '.' in x else x)
    format_data = df["Дата публикации"].to_list()
    new_data = []
    for date in format_data:
        new_data.append(f"{date[2]}-{date[1]}-{date[0]}")
    df["Дата публикации"] = new_data
    df["Дата публикации"] = df["Дата публикации"].astype("datetime64[ns]")

    # Форматируем таблицу
    df.columns = ["Профессия", "Зарплата от", "Населённый пункт", "Наниматель", "Дата публикации",
                  "Вакантных мест", "ID", "Дата сбора данных", "Вакансия", "Зарплата до", "Требуемый опыт работы", "Источник"]
    df = df[["Источник", "ID", "Профессия", "Вакансия", "Населённый пункт", "Требуемый опыт работы", "Зарплата от",
             "Зарплата до", "Дата публикации", "Дата сбора данных", "Наниматель", "Вакантных мест"]]
    return df


async def run_profzan():
    try:
        check_connection()
        print("Центр занятости: начинаем собирать данные")
        df = await get_profzan_data()
        df = filter_data(df)
        return df
    except Exception:
        print("Центр занятости: произошла ошибка. Сбор данных с источника остановлен.")


async def collect_to_excel():
    df_profzan = await run_profzan()
    today_date = datetime.date.today()
    path_to_export = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'Центр занятости',
                                  f"Центр занятости - {today_date}.xlsx")
    df_profzan.to_excel(path_to_export, sheet_name='Данные', index=False)


async def main():
    task = asyncio.create_task(collect_to_excel())
    await task


if __name__ == "__main__":
    asyncio.run(main())
