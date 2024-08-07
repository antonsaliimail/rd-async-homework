"""
У цьому домашньому завданні вам необхідно написати рішення для завантаження інформації з використанням асинхронного підходу.

Вимоги:

використати asyncio
застосувати aiohttp АБО httpx-бібліотеки
задіяти техніки використання timeout
вхідні параметри для скрипта — файл, де кожна лінія — це посилання на ресурс (використайте sys.argv або argparse, будь-що своє)
вміст відповіді зберігати у файлах
сповістити про всі timeout-помилки у консоль
Як буде оцінювати домашнє завдання:

скрипт вивантажує вміст посилань у файл
використано асинхронний підхід
застосовано timeout-техніки
користувач отримав сповіщення про timeout
Формат здачі завдання:

Оформіть отриманий результат на GitHub і прикріпіть посилання у відповідне поле в LMS до цього уроку.

"""
import argparse
import asyncio
import os
import re
from collections import Counter

import aiohttp


def get_file_name_from_url(url, count):
    # Remove protocol part (http, https)
    file_name = re.sub(r'^https?://', '', url)

    # Remove 'www.'
    file_name = re.sub(r'^www\.', '', file_name)

    # Replace any character that is not alphanumeric or underscore with underscore
    file_name = re.sub(r'[^a-zA-Z0-9]', '_', file_name)

    # Remove trailing underscores
    file_name = file_name.rstrip('_')

    # Add count if greater than 1
    if count > 1:
        file_name += f"_{count}"

    # Ensure the filename ends with .txt or another suitable extension
    file_name += ".txt"

    return file_name


def save_results(results):
    dest_dir = "downloaded_data"
    os.makedirs(dest_dir, exist_ok=True)

    # Track the number of times each file name has been used
    file_name_counter = Counter()

    for url, result in results:
        if isinstance(result, Exception):
            print(f"Error fetching {url}: {result}")
        else:
            # Increment the count for the URL
            file_name_counter[url] += 1

            # Get the unique file name
            dest_file_path = os.path.join(dest_dir, get_file_name_from_url(url, file_name_counter[url]))

            # Save result to the file
            with open(dest_file_path, "w") as f:
                f.write(result)


async def fetch_url(session, url, timeout):
    print(f"Fetching {url}")
    try:
        async with session.get(url, timeout=timeout) as response:
            result_text = await response.text()
            return url, result_text
    except asyncio.TimeoutError:
        return url, asyncio.TimeoutError("TimeoutError: Request to the url timed out.")
    except Exception as e:
        return url, e


async def main(input_file_path):
    # Read urls from file
    with open(input_file_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    # Create tasks
    tasks = []
    timeout = 1
    async with aiohttp.ClientSession() as session:
        for line in lines:
            tasks.append(fetch_url(session, line, timeout))

        # Wait for the tasks to be executed
        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Save results
    save_results(results)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--file", help="Path to the input file", required=True)

    parsed_args = arg_parser.parse_args()

    asyncio.run(main(parsed_args.file))
