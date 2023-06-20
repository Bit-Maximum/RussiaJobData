# Получение данных -> Объединение данных -> Создание/обновление Excel для дашборда
import sys
import os
import pandas as pd

from SourceCode.HHru import HHru
from SourceCode.FarPost import FarPost
from SourceCode.Profzan import Profzan

from SourceCode.Errors.ErrorMassages import FORMAT_ERROR

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
    return os.path.join(os.path.abspath(os.curdir), "Вакансии в Приморском крае.xlsx")


def get_recent_data():
    xlsx_path = get_path_to_data()
    if os.path.exists(xlsx_path):
        df_recent = pd.read_excel(xlsx_path, sheet_name="Данные")
        print(f"Обнаружены более ранние данные в файле {xlsx_path}")
    else:
        df_recent = pd.DataFrame(columns=["Источник", "ID", "Профессия", "Вакансия", "Населённый пункт",
                                          "Требуемый опыт работы", "Зарплата от", "Зарплата до", "Дата публикации",
                                          "Дата сбора данных", "Наниматель", "Вакантных мест"])
    return df_recent


async def collect_data(drop_duplicates=True):
    tasks = set_tasks()
    if not tasks:
        print("Выключены все источники: не от куда взять новые данные")
        return "NoActivTasks"

    new_data = await asyncio.gather(*tasks)
    dfs = [get_recent_data()]
    dfs.extend(new_data)

    total_df = pd.concat(dfs, ignore_index=True)
    if drop_duplicates:  # По умолчанию повторяющиеся строки удаляются
        total_df = total_df.drop_duplicates(subset=["ID"], keep="first", inplace=False)
    export_path = get_path_to_data()
    total_df.to_excel(export_path, sheet_name="Данные", index=False)
    print(f"Новые данные добавлены в файл '{export_path}'")
    wait = input("Для завершения программы нажмите 'Enter': ")


def update_data(drop_duplicates=True):
    asyncio.run(collect_data(drop_duplicates=drop_duplicates))


if __name__ == "__main__":
    delete_duplicates = False
    if len(sys.argv) > 1:
        delete_duplicates = bool(sys.argv[1])
    update_data(delete_duplicates)
