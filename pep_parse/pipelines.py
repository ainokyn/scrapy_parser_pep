# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import datetime as dt
from collections import Counter
from pathlib import Path

BASE_DIR = Path.cwd()


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
        self.csvwriter.writerow(['Статус', 'Количество'])

    def process_item(self, item, spider):
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
