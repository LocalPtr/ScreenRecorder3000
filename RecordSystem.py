import cv2
import numpy as np
import pyautogui
import dearpygui.dearpygui as dpg
import pygetwindow as gw
import functions as func
import keyboard


def start_recording(sender, app_data):
    dpg.disable_item(sender)
    dpg.set_value('info', 'Для завершения нажмите на клавиатуре [CTRL]+[Q]')
    now = func.now()
    if dpg.get_value('auto_name'):
        dpg.set_value('file_name', f"ScreenRecord {func.now()}")
    window_name = dpg.get_value('windows_title')
    # define the codec
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # frames per second
    fps = dpg.get_value('fps')
    # the time you want to record in seconds
    record_seconds = 3600
    # search for the window, getting the first matched window with the title
    w = gw.getWindowsWithTitle(window_name)[0]
    # activate the window
    w.activate()
    out = cv2.VideoWriter(f"Files\\{func.drs(dpg.get_value('file_name'))}.avi", fourcc, fps, tuple(w.size))
    for i in range(int(record_seconds * fps)):
        dpg.set_item_label(sender, f'Идет запись... {func.time_difference(now)}')
        img = pyautogui.screenshot(region=(w.left, w.top, w.width, w.height))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
        if dpg.get_value('screen_recorder'):
            cv2.imshow("screenshot", frame)
        if keyboard.is_pressed('ctrl+q'):
            break

    cv2.destroyAllWindows()
    out.release()
    dpg.set_value('info', '')
    dpg.enable_item(sender)
    dpg.set_item_label(sender, 'Начать запись')
