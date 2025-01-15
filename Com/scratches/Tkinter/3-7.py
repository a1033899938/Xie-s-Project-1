import tkinter
import tkinter.messagebox


# 用户登录验证
def login():
    name = entryName.get()
    pwd = entryPwd.get()
    if name == 'admin' and pwd == '123456':
        tkinter.messagebox.showinfo(title='userlogin', message='ok')
    else:
        tkinter.messagebox.showerror(title='userlogin', message='Error')


# 清空用户输入的用户名和密码
def cancel():
    varName.set('')
    varPwd.set('')


window = tkinter.Tk()
window.title('my window')
window.geometry('200x120')
varName = tkinter.StringVar(value='')
varPwd = tkinter.StringVar(value='')
# 创建标签
labelName = tkinter.Label(window, text='User Name:', justify=tkinter.RIGHT, width=80)
# 将标签放到窗口上
labelName.place(x=10, y=5, width=80, height=20)
# 创建文本框，并设置关联的变量
entryName = tkinter.Entry(window, width=80, textvariable=varName)
entryName.place(x=100, y=5, width=80, height=20)

labelPwd = tkinter.Label(window, text='User Pwd:', justify=tkinter.RIGHT, width=80)
labelPwd.place(x=10, y=30, width=80, height=20)
# 创建密码文本框
entryPwd = tkinter.Entry(window, show='*', width=80, textvariable=varPwd)
entryPwd.place(x=100, y=30, width=80, height=20)
# 创建按钮组件，同时设置按钮事件处理函数
buttonOk = tkinter.Button(window, text='Login', command=login)
buttonOk.place(x=30, y=70, width=50, height=20)
buttonCancel = tkinter.Button(window, text='Cancel', command=cancel)
buttonCancel.place(x=90, y=70, width=50, height=20)
# 启动消息循环
window.mainloop()


# 通过x，y设置的窗口/标签/按钮的位置，其原点坐标为上一个窗口/标签/按钮的左下角？