import tkinter

window = tkinter.Tk()
window.title('my window')
window.geometry('200x180')

l = tkinter.Label(
    window,
    text='this is label!',  # 标签文字
    bg='pink',  # 背景颜色
    font=('Arial', 12),  # 标签字体
    width=15, height=2  # 标签长宽
)

l.pack()  # 固定窗口位置

window.mainloop()

# 代码解释
# 创建了一个窗口并定义了它的标题和尺寸
# 在窗口中创建了一个标签，并定义了他的文本和字体、背景（是一个几何图形）颜色和长宽
# 固定了标签的位置，默认为窗口的居中靠上位置
# 显示了这个创建的主窗口


