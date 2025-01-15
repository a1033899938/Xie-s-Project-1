import tkinter

window = tkinter.Tk()
window.title('my window')
window.geometry('200x180')

# pack布局
l1 = tkinter.Label(window, text='this is label!', bg='pink', font=('Arial', 12),
                   width=15, height=2)
l1.pack(side='bottom')  # 将标签放在底部

# # grid布局
# for i in range(4):
#     for j in range(3):
#         tkinter.Label(window, text=1).grid(
#             row=i,  # 行
#             column=j,  # 列
#             padx=10,  # 单元格左右间距
#             pady=10  # 单元格上下间距
#         )

# place布局
l2 = tkinter.Label(window, text='This is Label2!', bg='green', justify=tkinter.RIGHT, width=50)
l2.place(x=40, y=50,  # 设置x，y坐标
         width=100, height=30  # 设置长宽
         )

window.mainloop()

# 代码解释
# 创建了两个标签
# 其中一个通过.pack(side = 'bottom')调整了其位置
# 另一个通过.place调整了其位置(左上角的位置)和标签背景的大小（可能会遮住一部分标签文本）

# 注意同一个程序中，只能定义一种布局，不能同时使用grid()和pack()方法。
