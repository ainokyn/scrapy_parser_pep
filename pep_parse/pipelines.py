import csv
import datetime as dt
from collections import Counter
from pathlib import Path

from scrapy.exceptions import DropItem

BASE_DIR = Path.cwd()
heading = ['Статус', 'Количество']


class PepParsePipeline:
    def __init__(self):
        self.list_status = []

    def open_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime('%Y-%m-%d-%H-%M-%S')
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = results_dir / file_name
        self.file = open(file_path, 'w', encoding='UTF-8', newline='')
        self.csvwriter = csv.writer(self.file)
        self.csvwriter.writerow(heading)

    def process_item(self, item, spider):
        if "status" not in item:
            raise DropItem('Ключ status отсутствует в словаре item.')
        else:
            self.list_status.append(item["status"])
        return item

    def close_spider(self, spider):
        total = len(self.list_status)
        count = Counter(self.list_status)
        st = list(count.keys())
        am = list(count.values())
        for stat, amount in list(zip(st, am)):
            self.csvwriter.writerow([stat, amount])
        self.csvwriter.writerow(['Total', total])
        self.file.close()
