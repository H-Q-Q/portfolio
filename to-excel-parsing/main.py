import pandas as pd
import os
from pprint import pprint


def main():
    root = os.getcwd()
    main_folders = [f for f in os.listdir(root) if os.path.isdir(f)]

    # Открыть файл на запись через ExcelWriter
    with pd.ExcelWriter('all_reports.xlsx', engine='xlsxwriter') as writer:
        current_row = 0  # Отслеживаем текущую строку для вставки данных

        for main_folder in main_folders:
            if main_folder == 'venv':
                continue

            # Поиск вложенной папки в каждой основной папке
            subfolders = [os.path.join(main_folder, subfolder) for subfolder in os.listdir(main_folder) if
                          os.path.isdir(os.path.join(main_folder, subfolder))]

            # Сортировка по сабфолдерам для обеспечения правильного порядка данных
            subfolders = sorted(subfolders,
                                key=lambda x: float(os.path.basename(x)) if os.path.basename(x).replace('.', '',
                                                                                                        1).isdigit() else x)

            for subfolder in subfolders:
                # Получаем файлы внутри вложенных папок
                file_names = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))]
                field_names = [f[:-4] for f in file_names if f.endswith('.dat')]
                data = {"h rel": []}

                first_is_parsed = False

                for file_name in file_names:
                    field = file_name[:-4]
                    data[field] = []
                    file_path = os.path.join(subfolder, file_name)

                    data_started = False
                    with open(file_path, 'r') as file:
                        lines = file.readlines()

                    for line in lines:
                        if '[Data]' in line:
                            data_started = True
                            continue
                        if data_started:
                            try:
                                parsed_line = [float(x) for x in line.strip().split(',')]
                            except ValueError:
                                continue

                            data[field].append(parsed_line[0])

                            if not first_is_parsed:
                                data["h rel"].append(parsed_line[1])

                    first_is_parsed = True

                df = pd.DataFrame(data, columns=["h rel"] + field_names)

                # Добавление строки с названием папки в первый столбец перед шапкой таблицы
                folder_name_df = pd.DataFrame({df.columns[0]: [f'Folder: {subfolder}']})

                # Запись названия папки в первую строку перед шапкой
                folder_name_df.to_excel(writer, startrow=current_row, index=False, header=False)

                # Затем записываем шапку и данные таблицы начиная со следующей строки
                df.to_excel(writer, startrow=current_row + 1, index=False, header=True)

                # Обновляем текущую строку, добавляя 2 пустые строки между таблицами
                current_row += len(df) + 3  # Длина данных + строка для названия папки + шапка + 2 пустые строки

                pprint(data)


if __name__ == "__main__":
    main()
