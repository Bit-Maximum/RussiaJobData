import os
from datetime import datetime
import json

import pandas as pd
import requests

import asyncio
from aiohttp import ClientSession

from SourceCode.HHru.profs import get_profs


# Пауза между запросами на API: TIME_OUT - в рамках одной вакансии, REGION_TIME_OUT - при смене региона/профессии
TIME_OUT = 2.5
REGION_TIME_OUT = 3


# Время выполнения программы: ~2 часа
def check_connection():
    print("Подключение к HH.ru: ", end="")
    url = 'https://api.hh.ru/vacancies'
    params = {
        "text": "Менеджер",
        "per_page": 1,
        "search_field": ["name", "description"]
    }

    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        print("OK")
        return
    else:
        print("Ошибка соединения. Сервис HH.ru не доступен.")
        raise Exception


async def get_city_id():
    async with ClientSession() as session:
        url = 'https://api.hh.ru/areas'
        async with session.get(url=url) as resp:
            js = await resp.json()
            regions_js = js[0]["areas"]

            for reg in regions_js:
                if reg.get("name") == "Приморский край":
                    prim = reg.get("areas")
                    break

            cities = {}
            top = ["Владивосток", "Артём", "Находка", "Уссурийск", "Арсеньев", "Большой Камень",
                   "Фокино (Приморский край)", "Спаск-Дальний", "Партизанск", "Лесозаводск", "Дальнегорск",
                   "Дальнереченск"]

            for city in prim:
                if city.get("name") in top:
                    cities[city.get("name")] = city.get("id")

            for city in prim:
                if city.get("name") not in top:
                    cities[city.get("name")] = city.get("id")

            return cities


async def get_page(vacancy: str, area=22, page=0):
    async with ClientSession() as session:
        url = 'https://api.hh.ru/vacancies'
        params = {
            "text": vacancy,
            "area": area,
            "page": page,
            "per_page": 100,
            "search_field": ["name", "description"]
        }
        async with session.get(url=url, params=params) as response:
            info = await response.read()
            return info


async def get_count(vacancy: str, area=22, page=0):
    for _ in range(3):  # Бросаем исключение, если по запросу не нашлось ни одной вакансии
        try:            # Но сначала проверяем второй раз - на случай, если это был просто пролаг
            async with ClientSession() as session:
                url = 'https://api.hh.ru/vacancies'
                params = {
                    "text": vacancy,
                    "area": area,
                    "page": page,
                    "per_page": 1,
                    "search_field": ["name", "description"]
                }
                async with session.get(url=url, params=params) as response:
                    count = await response.json()
                    res = count["found"]
                    return res
        except:
            await asyncio.sleep(REGION_TIME_OUT)
            continue
    # Если ничего не найдено, то HHru не возвращает ничего - поэтому вернём 0 вручную
    return 0


async def get_vacancies(vacancy, area):
    try:
        js_objs = []
        page_code = await get_page(vacancy, area)
        total_pages = json.loads(page_code)["pages"]
        await asyncio.sleep(TIME_OUT)
    except:
        return None

    for i in range(total_pages):  # Максимально можно получить только 2000 результатов (20 страниц по 100 элементов)
        try:
            js_code = await get_page(vacancy, area, i)
            js = json.loads(js_code)
            js_objs.extend(js["items"])
            await asyncio.sleep(TIME_OUT)
        except:
            await asyncio.sleep(TIME_OUT)
            continue
    if not js_objs:
        return None
    return js_objs



# Можете использовать свой собственный список профессий
def get_profs_from_file(path):
    profs = []
    with open(path, "r", encoding="UTF-8") as file:
        for line in file.readlines():
            profs.append(line.rstrip("\n"))
    return profs


async def get_hhru_data():
    current_date = datetime.now().date()
    profs = get_profs()

    city_ids = await get_city_id()
    prim_id = 1948
    dfs = []
    total_profs = len(profs)

    for num, prof in enumerate(profs):
        if num % 10 == 0:
            print(f"HH.ru: получено {num} из {total_profs} профессий")
        total_found = await get_count(prof, prim_id)
        if total_found > 0:
            if total_found > 2000:  # Если нельзя получить все объявления в Приморье сразу, то смотрим по каждому городу
                for city, city_id in city_ids.items():
                    found = await get_count(prof, city_id)

                    if found > 0:
                        temp = await get_vacancies(prof, city_id)
                        if temp is None:
                            continue
                        temp = pd.DataFrame(temp)
                        temp["Профессия"] = prof
                        temp["Дата сбора"] = current_date
                        dfs.append(temp)

                    await asyncio.sleep(REGION_TIME_OUT)
                    total_found -= found
                    if total_found < 1:
                        break
            else:  # Или сразу забираем все данные
                temp = await get_vacancies(prof, prim_id)
                if temp is None:
                    continue
                temp = pd.DataFrame(temp)
                temp["Профессия"] = prof
                temp["Дата сбора"] = current_date
                dfs.append(temp)

    total_df = pd.concat(dfs, ignore_index=True)
    return total_df


def filter_data(df):
    # Отключаем предупреждения
    pd.options.mode.chained_assignment = None  # default='warn'

    # Удаление лишних данных
    df = df.drop_duplicates(subset=["id"], keep="first", inplace=False)
    try:
        df = df.drop(['premium', 'department', 'has_test',
                      'response_letter_required', 'type', 'address',
                      'response_url', 'sort_point_distance', 'created_at',
                      'archived', 'apply_alternate_url', 'insider_interview', 'url',
                      'adv_response_url', 'alternate_url', 'relations', 'snippet',
                      'contacts', 'schedule', 'working_days', 'working_time_intervals',
                      'working_time_modes', 'accept_temporary', 'professional_roles',
                      'accept_incomplete_resumes', 'employment', 'immediate_redirect_url',
                      'immediate_redirect_vacancy_id'], axis=1)
    except:
        try:
            df = df.drop(
                ['premium', 'department', "has_test", "response_letter_required", "type", 'address', 'response_url',
                 'sort_point_distance', 'created_at', 'archived', 'apply_alternate_url', 'insider_interview', 'url',
                 'adv_response_url', 'alternate_url', 'relations', 'snippet',
                 'contacts', 'schedule', 'working_days', 'working_time_intervals',
                 'working_time_modes', 'accept_temporary', 'professional_roles',
                 'accept_incomplete_resumes', 'employment', "immediate_redirect_url"], axis=1)
        except:
            df = df.drop(['premium', 'department', 'has_test',
                          'response_letter_required', 'type', 'address',
                          'response_url', 'sort_point_distance', 'created_at',
                          'archived', 'apply_alternate_url', 'insider_interview', 'url',
                          'adv_response_url', 'alternate_url', 'relations', 'snippet',
                          'contacts', 'schedule', 'working_days', 'working_time_intervals',
                          'working_time_modes', 'accept_temporary', 'professional_roles',
                          'accept_incomplete_resumes', 'employment'], axis=1)

    # Восстанавливаем недостающие столбцы
    df["Вакантных мест"] = 1
    df["Зарплата до"] = df["salary"]
    df["Источник"] = "HH.ru"

    # Получаем значения атрибутов из "сырых" данных
    df["area"] = df["area"].apply(lambda x: x.get("name") if x is not None else "")
    df["Зарплата до"] = df["Зарплата до"].apply(lambda x: x.get("to") if x is not None else "")
    df["salary"] = df["salary"].apply(lambda x: x.get("from") if x is not None else "")
    df["employer"] = df["employer"].apply(lambda x: x.get("name") if x is not None else "")
    df["experience"] = df["experience"].apply(lambda x: x.get("name") if x is not None else "")
    df["published_at"] = df["published_at"].apply(lambda x: x.split("T")[0] if "T" in x else "")

    # Меняем тип данных
    df["published_at"] = df["published_at"].astype("datetime64[ns]")
    df["Дата сбора"] = df["Дата сбора"].astype("datetime64[ns]")

    # Форматируем таблицу
    df.columns = ["ID", "Вакансия", "Населённый пункт", "Зарплата от", "Дата публикации", "Наниматель",
                  "Требуемый опыт работы", "Профессия", "Дата сбора данных", "Вакантных мест", "Зарплата до", "Источник"]

    df = df[["Источник", "ID", "Профессия", "Вакансия", "Населённый пункт", "Требуемый опыт работы", "Зарплата от",
             "Зарплата до", "Дата публикации", "Дата сбора данных", "Наниматель", "Вакантных мест"]]
    return df


async def run_hhru():
    check_connection()
    print("HHru: начинаем собирать данные")
    df = await get_hhru_data()
    print("HHru: фильтрация данных")
    df = filter_data(df)
    print("HHru: собор данных завершён")
    return df


async def collect_to_excel():
    df_hhru = await run_hhru()
    current_date = datetime.now().date()
    path_to_export = os.path.join(os.path.dirname(__file__), f"HHru - {current_date}.xlsx")
    df_hhru.to_excel(path_to_export, sheet_name='Данные', index=False)


async def main():
    task = asyncio.create_task(collect_to_excel())
    await task


if __name__ == "__main__":
    asyncio.run(main())

