import os
import time


def monitor_with_changes():
    path = "."

    file_info = {}
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            file_info[file] = os.path.getmtime(file_path)

    print("Мониторинг изменений...")

    try:
        while True:
            time.sleep(2)
            current_files = os.listdir(path)

            # Проверяем новые файлы
            for file in current_files:
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):
                    if file not in file_info:
                        print(f"Создан файл: {file}")
                        file_info[file] = os.path.getmtime(file_path)
                    else:
                        # Проверяем изменения
                        old_time = file_info[file]
                        new_time = os.path.getmtime(file_path)
                        if new_time != old_time:
                            print(f"Изменен файл: {file}")
                            file_info[file] = new_time

            # Проверяем удаленные файлы
            for file in list(file_info.keys()):
                if file not in current_files:
                    print(f"Удален файл: {file}")
                    del file_info[file]

    except KeyboardInterrupt:
        print("!Остановлено!")


# Запуск

monitor_with_changes()
