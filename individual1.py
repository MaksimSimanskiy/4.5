#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Выполнить индивидуальное задание лабораторной работы 4.5, использовав классы данных, а
также загрузку и сохранение данных в формат XML.
"""

from dataclasses import dataclass, field
import sys
from typing import List


@dataclass(frozen=True)
class Shops:
    name: str
    product: str
    price: int


@dataclass
class Store:
    shops: List[Shops] = field(default_factory=lambda: [])

    def add(self, name: str, product: str, price: int) -> None:
        self.shops.append(
            Shops(
                name=name,
                product=product,
                price=price
            )
        )
        self.shops.sort(key=lambda Shops: Shops.name)

    def __str__(self) -> str:
        # Заголовок таблицы.
        table = []
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 8
        )
        table.append(line)
        table.append(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "No",
                "Магазин.",
                "Товар",
                "Цена"
            )
        )
        table.append(line)
        for idx, Shops in enumerate(self.shops, 1):
            table.append(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    Shops.name,
                    Shops.product,
                    Shops.price
                )
            )
        table.append(line)
        return '\n'.join(table)

    def select(self, name: str) -> None:
        cout: int = 0
        for i, shop in enumerate(self.shops, 1):
            if (shop.name == name):
                cout +=1
                print(
                    ' |{} -  {:<5} |{} -  {:<5} |'.format('product',
                        shop.product,'price',
                        shop.price
                    )
                )
        if(cout == 0):
            print("Такого магазина нет")

    def load(self, filename: str) -> None:
        with open(filename, 'r', encoding='utf8') as fin:
            xml: str = fin.read()
            parser = ET.XMLParser(encoding="utf8")
            tree = ET.fromstring(xml, parser=parser)
            self.shops = []
            for shop_element in tree:
                name, product, price = None, None, None
                for element in shop_element:
                    if element.tag == 'name':
                        name = element.text
                    elif element.tag == 'product':
                        product = element.text
                    elif element.tag == 'price':
                        price = int(element.text)
                    if name is not None and product is not None \
                            and price is not None:
                        self.shops.append(
                            Shops(
                                name=name,
                                product=product,
                                price=price
                            )
                        )


if __name__ == '__main__':
    Store = Store()
    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()
        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break
        elif command == 'add':
            # Запросить данные
            name = input("Название магазина? ")
            product = input("Товар? ")
            price = int(input("Цена? "))
            Store.add(name, product, price)
        elif command == 'list':
            # Вывести список.
            print(Store)
        elif command.startswith('select '):
            parts = command.split(maxsplit=1)
            print(parts[1])
            selected = Store.select(parts[1])
        elif command.startswith('load '):
            parts = command.split(maxsplit=1)
            Store.load(parts[1])
        elif command.startswith('save '):
            # Разбить команду на части для имени файла.
            parts = command.split(maxsplit=1)
            # Сохранить данные в файл.
            Store.save(parts[1])
        elif command == 'help':
            print("Список команд:\n")
            print("add - добавить магазин;")
            print("list - вывести список магазинов;")
            print("select <магазин> - вывести товары из магазина;")
            print("load <имя_файла> - загрузить данные из файла;")
            print("save <имя_файла> - сохранить данные в файл;")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)