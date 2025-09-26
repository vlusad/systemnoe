import os
import time


def monitor_with_changes():
    path = "."

    file_info = {}
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            file_info[file] = os.path.getmtime(file_path)

    print("Мониторинг изменений................")

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












import os
import time
import stat


def full_low_level_monitor():
    """Полный низкоуровневый мониторинг с отслеживанием изменений файлов"""

    # Выбираем доступную директорию
    path = "C:/4321-23/усачев"
    print(f"Мониторим директорию: {path}")

    # Проверяем доступ
    try:
        test_fd = os.open(path, os.O_RDONLY)
        os.close(test_fd)
    except PermissionError:
        print("Нет доступа к директории")
        return

    print("Отслеживаем: создание, удаление, изменение файлов")
    print("Нажмите Ctrl+C для остановки\n")

    # Кэш для хранения информации о файлах
    file_cache = {}  # {inode: {'name': filename, 'mtime': mtime, 'size': size}}

    try:
        while True:
            try:
                dir_fd = os.open(path, os.O_RDONLY)
                files = os.listdir(path)

                current_files = {}

                # Сканируем файлы в директории
                for filename in files:
                    try:
                        file_path = os.path.join(path, filename)
                        fd = os.open(file_path, os.O_RDONLY)
                        st = os.fstat(fd)

                        if stat.S_ISREG(st.st_mode):  # Только обычные файлы
                            current_files[st.st_ino] = {
                                'name': filename,
                                'mtime': st.st_mtime,  # время изменения
                                'size': st.st_size  # размер файла
                            }

                        os.close(fd)
                    except (PermissionError, OSError):
                        continue

                os.close(dir_fd)

                # Проверяем новые файлы
                for inode, info in current_files.items():
                    if inode not in file_cache:
                        print(f"СОЗДАН: {info['name']} (размер: {info['size']} байт)")

                # Проверяем удаленные файлы
                for inode, info in list(file_cache.items()):
                    if inode not in current_files:
                        print(f"УДАЛЕН: {info['name']}")

                # Проверяем изменения в существующих файлах
                for inode, current_info in current_files.items():
                    if inode in file_cache:
                        old_info = file_cache[inode]
                        changes = []

                        # Проверяем изменение размера
                        if current_info['size'] != old_info['size']:
                            size_diff = current_info['size'] - old_info['size']
                            change_type = "увеличился" if size_diff > 0 else "уменьшился"
                            changes.append(f"размер {change_type} на {abs(size_diff)} байт")

                        # Проверяем изменение времени модификации
                        if current_info['mtime'] != old_info['mtime'] and current_info['size'] == old_info['size']:
                            changes.append("изменено содержимое")

                        # Если есть изменения - выводим уведомление
                        if changes:
                            print(f"ИЗМЕНЕН: {current_info['name']} ({', '.join(changes)})")

                # Обновляем кэш
                file_cache = current_files

                time.sleep(2)  # Проверка каждые 2 секунды

            except Exception as e:
                print(f"Ошибка сканирования: {e}")
                time.sleep(3)

    except KeyboardInterrupt:
        print("\nМониторинг остановлен")


# Запуск
full_low_level_monitor()


