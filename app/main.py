import re
import asyncio
import aiohttp
import argparse


# Регулярные выражения для наших проверок
URL_TESTS = re.compile(
    r'^(?:http|ftp)s?://'  # http:// или https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # доменные имена
    r'localhost|'  # localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IP-адрес IPv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IP-адрес IPv6
    r'(?::\d+)?'  # порт
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# Реализововаем функцию для проверки методов
def is_valid_url(url):
    return re.match(URL_TESTS, url) is not None


# Пишем асинхронную функцию(попробовал синхронно - но программа очень медленно работала, пришлось перейти на async)
async def check_methods(session: aiohttp.ClientSession, url: str) -> dict:
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']
    result = {}

    for method in methods:
        try:
            async with session.request(method, url) as response:
                if response.status != 405:  # Проверяем...
                    result[method] = response.status

        except Exception as e:
            # Ловим любые ошибки запроса и пропускаем
            result[method] = f'Ошибка: {e}'

    return result


# Пишем основную функцию
async def main(urls):
    results = {}
    async with aiohttp.ClientSession() as session:
        for url in urls:
            if is_valid_url(url):
                print(f'Переданная ссылка: "{url}" -> проверяется...')
                methods_status = await check_methods(session, url)
                results[url] = methods_status
            else:
                print(f'Строка "{url}" не является ссылкой')
    return results


# CLI
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI для проверки доступных HTTP методов по ссылкам')
    parser.add_argument('urls', metavar='URL', type=str, nargs='+', help='Список строк для проверки')

    args = parser.parse_args()

    # Асинхронные задачи
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(args.urls))

    # Результат
    print(results)