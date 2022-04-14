#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Для своего варианта лабораторной работы 2.17 добавьте возможность
хранения файла данных в домашнем каталоге пользователя.
Для выполнения операций с файлами необходимо использовать модуль pathlib
"""

import json
import click
import pathlib


@click.group()
def group():
    pass


@group.command()
@click.argument('file_name')
@click.option("-n", "--name")
@click.option("-p", "--product")
@click.option("-pr", "--price")
def get_shop(file_name: str, name: str, product: str, price: int) -> list:
    shops_load: list = load_shops(file_name)
    shops_load.append({
        'name': name,
        'product': product,
        'price': price,
    })

    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(shops_load, fout, ensure_ascii=False, indent=4)
    return shops_load


@group.command()
@click.argument('file_name')
def display_shops(file_name: str) -> None:
    shops_load: list = load_shops(file_name)
    if shops_load:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 8,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "No",
                "Название.",
                "Товар",
                "Цена"
            )
        )
        print(line)
        for idx, shop in enumerate(shops_load, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(

                    idx,
                    shop.get('name', ''),
                    shop.get('product', ''),
                    shop.get('price', 0)

                )
            )
            print(line)


@group.command()
@click.argument('file_name')
@click.option("-n", "--name")
def select_shops(file_name: str, name: str) -> None:
    shops_load: list = load_shops(file_name)
    cout = 0
    for i, shop in enumerate(shops_load, 1):
        if shop.get('name') == name:
            cout = 1
            print(
                ' | {:<5} | {:<5} '.format(
                    shop.get('product', ''),
                    shop.get('price', 0),
                )
            )
        elif cout == 0:
            print("Такого магазина нет")


@group.command()
@click.argument('file_name')
def save_home(file_name: str) -> None:
    current: pathlib.Path = pathlib.Path.cwd().joinpath(file_name)
    homepath = pathlib.Path.home().joinpath(file_name)
    with homepath.open(mode='xb') as fid:
        fid.write(current.read_bytes())


def load_shops(file_name) -> list:
    with open(file_name, "r", encoding="utf-8") as fin:
        loadfile: list = json.load(fin)
    return loadfile


def main():
    group()


if __name__ == '__main__':
    main()
