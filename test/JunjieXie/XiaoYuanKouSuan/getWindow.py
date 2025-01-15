import pygetwindow as gw
import win32gui
import win32con
import time


def print_all_window_titles():
    window_titles = gw.getAllTitles()
    valid_window_title = [win for win in window_titles if win.strip() and '任务栏' not in win]
    for i, title in enumerate(valid_window_title):
        print(f'{i}: {title}')
    return valid_window_title


def get_window(title):
    window = gw.getWindowsWithTitle(title)[0]
    return window


def wakeup_window_by_title(window_title):
    # 只通过窗口标题查找窗口句柄
    hwnd = win32gui.FindWindow(None, window_title)

    if hwnd == 0:
        print(f"未找到标题为 '{window_title}' 的窗口")
        return

    # 使用 ShowWindow 将窗口恢复并置于最前方
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 如果窗口最小化，恢复它
    win32gui.SetForegroundWindow(hwnd)  # 将窗口设置为前台窗口
    print(f"窗口 '{window_title}' 已被唤醒并置于前台")


if __name__ == "__main__":
    # track_first_taskbar_window(4)
    # get_taskbar_window(4)
    window_titles = print_all_window_titles()
    window_title = '雷电模拟器'
    window = get_window(window_title)
    wakeup_window_by_title(window_title)