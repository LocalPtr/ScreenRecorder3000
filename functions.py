import webbrowser
import os
import pyautogui
import dearpygui.dearpygui as dpg
from pywinauto import Desktop
import datetime
from dateutil.relativedelta import relativedelta


def open_url(sender, app_data, user_data):
    return webbrowser.open('https://t.me/bysandj')


def open_files_folder(sender, app_data, user_data):
    webbrowser.open(f'{os.getcwd()}\\Files')


def get_windows_title():
    windows_title_list = []
    windows = pyautogui.getAllWindows()
    for window in windows:
        if window.title != '':
            windows_title_list.append(window.title)
    return windows_title_list


def refresh_window_title(sender, app_data, user_data):
    windows = Desktop(backend="uia").windows()
    dpg.configure_item('windows_title', items=get_windows_title())


def drs(text):
    # decode_russian_symbols
    # 848
    lower_case = [224, 255]
    upper_case = [192, 223]
    yo_bl = [168, 184]  # big - little
    # 1025 - 1105
    result = ''
    for i in text:
        if (lower_case[0] <= ord(i) <= lower_case[1]) or (upper_case[0] <= ord(i) <= upper_case[1]):
            result += f'{chr(ord(i) + 848)}'
        else:
            result += i
    return result


def file_system(sender, app_data, user_data):
    if f"{dpg.get_value('file_name')}.avi" in os.listdir(f'{os.getcwd()}\\Files'):
        dpg.set_value('warning', 'Такой файл уже существует!')
    else:
        dpg.set_value('warning', '')


def limit(sender, app_data, user_data):
    if app_data > 120:
        dpg.set_value(sender, 120)
    elif app_data < 5:
        dpg.set_value(sender, 5)


def auto_create_filename(sender, app_data, user_data):
    if dpg.get_value(sender):
        dpg.configure_item('file_name', readonly=True)
    else:
        dpg.configure_item('file_name', readonly=False)


def now() -> datetime.datetime.strftime:
    today = datetime.datetime.now()
    return today.strftime("%H-%M-%S %d-%m-%Y")


def time_difference(time_now: str) -> str:
    try:
        start = datetime.datetime.strptime(time_now, "%H-%M-%S %d-%m-%Y")
    except ValueError:
        start = datetime.datetime.strptime(now(), "%H-%M-%S %d-%m-%Y")
    ends = datetime.datetime.strptime(now(), "%H-%M-%S %d-%m-%Y")
    difference = relativedelta(ends, start)
    t_seconds = difference.seconds
    t_minutes = difference.minutes
    if t_minutes < 10:
        t_minutes = f'0{difference.minutes}'
    if t_seconds < 10:
        t_seconds = f'0{difference.seconds}'
    return f'{t_minutes}:{t_seconds}'
