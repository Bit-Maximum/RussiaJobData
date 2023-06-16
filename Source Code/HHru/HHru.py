import os
from datetime import datetime
import time
import json

import requests as r
import pandas as pd



# Пауза между запросами на API: TIME_OUT - в рамках одной вакансии, REGION_TIME_OUT - при смене региона/профессии
TIME_OUT = 1
REGION_TIME_OUT = 1.5


# Время выполнения программы: ~2 часа
def check_connection():
    print("Подключение к HH.ru: ", end="")
    params = {
        "text": "Менеджер",
        "per_page": 1,
        "search_field": ["name", "description"]
    }
    response = r.get("https://api.hh.ru/vacancies", params=params)
    if response.status_code == 200:
        print("OK")
        return
    else:
        print("Ошибка соединения. Сервис HH.ru не доступен.")
        raise Exception


def get_region_city_id():
    resp = r.get("https://api.hh.ru/areas")
    js = json.loads(resp.content.decode())
    regions_js = js[0]["areas"]

    regions = dict()
    for region in regions_js:
        cities = dict()
        for city in region["areas"]:
            cities[city.get("name")] = city.get("id")
        regions[region.get("name")] = (region.get("id"), cities)

    return regions


def get_page(vacancy: str, area=22, page=0):
    params = {
        "text": vacancy,
        "area": area,
        "page": page,
        "per_page": 100,
        "search_field": ["name", "description"]
    }
    response = r.get("https://api.hh.ru/vacancies", params=params)
    info = response.content.decode()
    return info


def get_count(vacancy: str, area=22, page=0):
    params = {
        "text": vacancy,
        "area": area,
        "page": page,
        "per_page": 1,
        "search_field": ["name", "description"]
    }
    response = r.get("https://api.hh.ru/vacancies", params=params)
    count = json.loads(response.content.decode())["found"]
    return count


def get_vacancies(vacancy, area):
    js_objs = []
    total_pages = json.loads(get_page(vacancy, area))["pages"]
    time.sleep(TIME_OUT)
    for i in range(total_pages):  # Максимально можно получить только 2000 результатов (20 страниц по 100 элементов)
        js = json.loads(get_page(vacancy, area, i))
        js_objs.extend(js["items"])
        time.sleep(TIME_OUT)
    return js_objs


def get_profs():
    profs = []
    with open("profs.txt", "r", encoding="UTF-8") as file:
        for line in file.readlines():
            profs.append(line.rstrip("\n"))
    return profs


def get_hhru_data():
    current_date = datetime.now().date()
    profs = get_profs()
    reg_city_ids = get_region_city_id()
    prim_id = 1948
    dfs = []
    total_profs = len(profs)

    for num, prof in enumerate(profs):
        if num % 50 == 0:
            print(f"HH.ru: получено {num} из {total_profs} профессий")
        total_found = get_count(prof, prim_id)
        if total_found > 0:
            if total_found > 2000:  # Если нельзя получить все объявления в Приморье сразу, то смотрим по каждому городу
                for city, city_id in reg_city_ids["Приморский край"][1].items():
                    found = get_count(prof, city_id)

                    if found > 0:
                        temp = pd.DataFrame(get_vacancies(prof, city_id))
                        temp["Профессия"] = prof
                        temp["Дата сбора"] = current_date
                        dfs.append(temp)

                    time.sleep(REGION_TIME_OUT)
                    total_found -= found
                    if total_found < 1:
                        break
            else:  # Или сразу забираем все данные
                temp = pd.DataFrame(get_vacancies(prof, prim_id))
                temp["Профессия"] = prof
                temp["Дата сбора"] = current_date
                dfs.append(temp)

    total_df = pd.concat(dfs, ignore_index=True)
    return total_df


def filter_data(df):
    # Удаление лишних данных
    df = df.drop_duplicates(subset=["id"])
    df = df.drop(['premium', 'department', "has_test", "response_letter_required", "type", 'address', 'response_url',
                  'sort_point_distance', 'created_at', 'archived', 'apply_alternate_url', 'insider_interview', 'url',
                  'adv_response_url', 'alternate_url', 'relations', 'snippet',
                  'contacts', 'schedule', 'working_days', 'working_time_intervals',
                  'working_time_modes', 'accept_temporary', 'professional_roles',
                  'accept_incomplete_resumes', 'employment'], axis=1)

    # Получаем значения атрибутов из "сырых" данных
    df["Вакантных мест"] = 1
    df["Зарплата до"] = df["salary"]
    df["area"] = df["area"].apply(lambda x: x.get("name") if x is not None else "")
    df["Зарплата до"] = df["Зарплата до"].apply(lambda x: x.get("to") if x is not None else "")
    df["salary"] = df["salary"].apply(lambda x: x.get("from") if x is not None else "")
    df["employer"] = df["employer"].apply(lambda x: x.get("name") if x is not None else "")
    df["experience"] = df["experience"].apply(lambda x: x.get("name") if x is not None else "")

    # Меняем тип данных
    df["published_at"] = df["published_at"].astype("datetime64[ns]")
    df["Дата сбора"] = df["Дата сбора"].astype("datetime64[ns]")
    df["id"] = df["id"].astype("int64")

    # Форматируем таблицу
    df.columns = ["ID", "Вакансия", "Населённый пункт", "Зарплата от", "Дата публикации", "Наниматель",
                  "Требуемый опыт работы", "Профессия", "Дата сбора данных", "Зарплата до", "Вакантных мест"]
    df = df[["ID", "Профессия", "Вакансия", "Населённый пункт", "Требуемый опыт работы", "Зарплата от",
             "Зарплата до", "Дата публикации", "Дата сбора данных", "Наниматель", "Вакантных мест"]]
    return df


def run_hhru():
    try:
        check_connection()
        print("HHru: начинаем собирать данные")
        df = get_hhru_data()
        df = filter_data(df)
        return df
    except Exception:
        return -1


if __name__ == "__main__":
    df_hhru = run_hhru()
    current_date = datetime.now().date()
    path_to_export = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'HHru', f"HHru - {current_date}.xlsx")
    df_hhru.to_excel(path_to_export, sheet_name='Данные', index=False)

