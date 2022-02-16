from pyrogram import Client
from lxml import html
import re

from requests import get
from random import choice
from time import sleep, perf_counter


def scrabThePage(page_number, compliment_lst):
    link = f"https://datki.net/komplimenti/zhenshine/page/{page_number}/"
    print(link)
    page = get(link)
    tree = html.fromstring(page.content)
    compliment_lst.extend(
        tree.xpath('//a[@class="post-copy btn"]/@data-clipboard-text')
    )


def message(sendToUsername, compliment_lst):
    API_ID = 0000000000
    API_HASH = ""
    app = Client("Don 't give it to anyone", API_ID, API_HASH) 
    rand_comp = choice(compliment_lst)

    with app:
        app.send_message(sendToUsername, rand_comp)

    print(f"ОТПРАВЛЕН КОМПЛИМЕНТ: {rand_comp}")


def new_page():
    compliment_lst = []
    print(f"Сбор комплиментов\n")
    start = perf_counter()
    total_pages = 1
    while total_pages <= 6:
        scrabThePage(total_pages, compliment_lst)
        total_pages += 1

    end = perf_counter()
    all_the_time = end - start
    print(f"Сбор комплиментов закончился за {round(all_the_time, 3)} sec[OK]\n")
    return compliment_lst


def check_username(sendToUsername):
    mask = re.compile('[a-zA-Z0-9_]')
    status_code = "[OK]"

    if not mask.search(sendToUsername):
        print(f"Введенное имя пользователя содержит недопустимые символы\n")
        sendToUsername = "vladimirpitun"
        status_code = "[AUTO]"

    print(f"Имя пользователя: {sendToUsername} {status_code}")
    return sendToUsername


def receiving_and_verifying_a_compliment(min_compl_len, compliment_lst):
    res_compliment = []
    mask = re.compile('[0-9]')
    status_code = "[OK]"

    if not mask.search(min_compl_len):
        min_compl_len = 10
        status_code = "AUTO"

    print(f"Минимальная длина комплимента: {min_compl_len} {status_code}\n")
    sleep(2)

    for compliment in compliment_lst:
        if len(compliment) > int(min_compl_len):
            res_compliment.append(compliment)

    if len(res_compliment) == 0:
        print("Для указанной минимальной длины не найдено ни одного комплимента. Попробуйте уменьшить значение")
        exit()

    return res_compliment


if __name__ == "__main__":
    compliment_lst = new_page()
    res_compliment = receiving_and_verifying_a_compliment(
        input("MIN_LEN: "), 
        compliment_lst
    )

    sendToUsername = check_username(
        input("USERNAME, которому хотите отправить комплимент: ")
    )

    while True:
        is_exit = input("Ожидание нажатия кнопки...\n")
        if is_exit == "exit":
            exit()
        else:
            message(sendToUsername, res_compliment)
