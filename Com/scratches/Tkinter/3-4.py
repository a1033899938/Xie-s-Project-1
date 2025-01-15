import tkinter

window = tkinter.Tk()
window.title('my window')
window.geometry('200x120')

# 定义button
b = tkinter.Button(window,
                   text='退出',  # 按钮的文字
                   bg='pink',  # 背景颜色
                   width=15, height=2,  # 设置长宽
                   command=window.quit  # 响应事件：关闭窗口
                   )
b.pack()

window.mainloop()