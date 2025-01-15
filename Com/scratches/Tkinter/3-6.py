import tkinter
import tkinter.messagebox

window = tkinter.Tk()
window.title('my window')
window.geometry('200x100')


def say_hello():
    tkinter.messagebox.showinfo(title='my message', message='hello!')


# 定义消息对话框
b = tkinter.Button(window, text="click", command=say_hello)
b.pack()

window.mainloop()

# 代码解释
# 通过tkinter.messagebox.showinfo可以显示一个消息弹窗