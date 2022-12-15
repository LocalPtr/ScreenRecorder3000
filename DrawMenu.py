import dearpygui.dearpygui as dpg
from RecordSystem import start_recording
import functions as func
import sys
import os

dpg.create_context()
size_height = 325
size_width = 600


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


txtr_link = resource_path("link.png")
txtr_refresh = resource_path("refresh.png")
width_link_btn, height_link_btn, channels_link_btn, data_link_btn = dpg.load_image(txtr_link)
width_refresh_btn, height_refresh_btn, channels_refresh_btn, data_refresh_btn = dpg.load_image(txtr_refresh)


def FirstOpen():
    try:
        os.mkdir(f'{os.getcwd()}\\Files')
    except FileExistsError:
        pass


with dpg.texture_registry():
    dpg.add_static_texture(width=width_link_btn, height=height_link_btn, default_value=data_link_btn,
                           tag="Texture_link")
    dpg.add_static_texture(width=width_refresh_btn, height=height_refresh_btn, default_value=data_refresh_btn,
                           tag="Texture_refresh")

with dpg.font_registry():
    with dpg.font(f'C:\\Windows\\Fonts\\calibri.ttf', 20, default_font=True, id="Default font"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        # remapping capital and small "ё"
        dpg.add_char_remap(0xa8, 0x401)
        dpg.add_char_remap(0xb8, 0x451)
        # set counter value equal to utf8 code of Russian capital "А" with consequent remapping from "А" to "я"
        utf = 0x410
        for i in range(0xc0, 0x100):
            dpg.add_char_remap(i, utf)
            utf += 1
    dpg.bind_font("Default font")


def add_info_text(sign, message, color_sign: tuple = (182, 182, 182), color_text: tuple = (255, 255, 255)):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text(sign, color=color_sign)
    with dpg.tooltip(t):
        dpg.add_text(message, color=color_text)


with dpg.window(tag="Primary Window", autosize=True):
    FirstOpen()
    dpg.add_spacer()
    with dpg.group(horizontal=True, tag='auto_search'):
        dpg.add_combo(func.get_windows_title(), default_value="Program Manager", tag='windows_title', width=350)
        dpg.add_image_button('Texture_refresh', callback=func.refresh_window_title, tag='Refresh_img')
        add_info_text('( i )', 'Для записи всего экрана выберите "Program Manager"')
    with dpg.group(horizontal=True):
        dpg.add_input_text(label='Название видео', default_value='output', tag='file_name',
                           callback=func.file_system, width=350)
        dpg.add_checkbox(label='авто', callback=func.auto_create_filename, tag='auto_name')
    dpg.add_slider_int(label='Скорость', max_value=120, min_value=5, default_value=15, tag='fps',
                       callback=func.limit, width=350)
    with dpg.group(horizontal=True):
        dpg.add_button(label='Открыть папку', callback=func.open_files_folder, width=350)
        dpg.add_image_button('Texture_link', callback=func.open_url)
        add_info_text('[v0.2]', 'Screen Recorder 3000 [version 0.2 BETA]', (80, 200, 120))
    dpg.add_spacer()
    with dpg.group():
        with dpg.child_window(height=73, width=size_width - 30):
            dpg.add_text('', tag='info')
            dpg.add_text('', tag='warning', color=(235, 76, 66))
    dpg.add_button(label='Начать запись', callback=start_recording, tag='start_record', width=size_width - 30,
                   height=60, pos=[8, 215])

dpg.create_viewport(title='Screen Recorder 3000', width=size_width, height=size_height, max_width=size_width,
                    min_width=size_width, max_height=size_height, min_height=size_height,
                    small_icon='icon.ico')

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
