# Получение данных -> Объединение данных -> Создание/обновление Excel для дашборда

import os
import pandas as pd

from SourceCode.HHru import HHru
from SourceCode.FarPost import FarPost
from SourceCode.Profzan import Profzan

import asyncio


# Включение/выключение источников данных
TO_RUN = {
    "HHru": True,
    "FarPost": True,
    "Profzan": True
}


def set_tasks():
    tasks_to_run = []

    if TO_RUN["HHru"]:
        tasks_to_run.append(asyncio.create_task(HHru.run_hhru()))
    if TO_RUN["FarPost"]:
        tasks_to_run.append(asyncio.create_task(FarPost.run_farpost()))
    if TO_RUN["Profzan"]:
        tasks_to_run.append(asyncio.create_task(Profzan.run_profzan()))

    return tasks_to_run


def get_path_to_data():
    return os.path.join(os.path.dirname(__file__), "Вакансии в Приморском крае.xlsx")


def get_recent_data():
    xlsx_path = get_path_to_data()
    if os.path.exists(xlsx_path):
        df_recent = pd.DataFrame.read_excel(xlsx_path, sheet_name="Данные")
    else:
        df_recent = pd.DataFrame(columns=["Источник", "ID", "Профессия", "Вакансия", "Населённый пункт",
                                          "Требуемый опыт работы", "Зарплата от", "Зарплата до", "Дата публикации",
                                          "Дата сбора данных", "Наниматель", "Вакантных мест"])
    return df_recent


async def collect_data():
    tasks = set_tasks()
    if not tasks:
        print("Выключены все источники: не от куда взять новые данные")
        return "NoActivTasks"

    new_data = await asyncio.gather(*tasks)
    dfs = [get_recent_data()]
    dfs.extend(new_data)
    total_df = pd.concat(dfs, ignore_index=True)
    total_df.drop_duplicates(subset=["ID"])

    xlsx_path = get_path_to_data()
    total_df.to_excel(xlsx_path, sheet_name="Данные", index=False)
    print("Новые данные добавлены в файл 'Вакансии в Приморском крае.xlsx'")


def update_data():
    asyncio.run(collect_data())


if __name__ == "__main__":
    update_data()
