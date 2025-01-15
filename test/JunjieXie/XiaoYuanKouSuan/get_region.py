from pynput import mouse

# 全局变量，用于存储鼠标的按下和松开位置
start_position = None
end_position = None


def on_click(x, y, button, pressed):
    global start_position, end_position

    if pressed:
        # 记录鼠标按下时的位置
        start_position = (x, y)
        print(f"鼠标按下位置: {start_position}")
    else:
        # 记录鼠标松开时的位置
        end_position = (x, y)
        print(f"鼠标松开位置: {end_position}")

        # 停止监听
        return False


def record_mouse_positions():
    # 创建一个鼠标监听器，当有点击时调用 on_click 方法
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


if __name__ == "__main__":
    print("请按下鼠标以记录位置，松开以记录第二个位置")
    record_mouse_positions()
    print(f"记录的起始位置: {start_position}, 结束位置: {end_position}")
    print(f"宽度: {end_position[0] - start_position[0]}, 高度: {end_position[1] - start_position[1]}")
