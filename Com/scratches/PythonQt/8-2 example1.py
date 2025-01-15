from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox


def MyMethod1():
    info = textEdit.toPlainText()
    salary_above_20k = ''
    salary_below_20k = ''
    for line in info.splitlines():
        if not line.strip():
            continue
        parts = line.split(' ')
        # 去掉列表中的空字符串内容
        parts = [p for p in parts if p]     # 以for p in parts开始循环，每次输出p，但是要输出前经过判断：if p（p是不是不为空），如果p为空，则跳过输出
        name, salary, age = parts
        if int(salary) >= 20000:
            salary_above_20k += name + '\n'
        else:
            salary_below_20k += name + '\n'

    QMessageBox.about(window,
                      '统计结果',
                      f'''薪资20000 以上的有：\n{salary_above_20k}
                    \n薪资20000 以下的有：\n{salary_below_20k}'''
                      )

app = QApplication([])  # 管理底层的

window = QMainWindow()  # 先定义主窗口（还并创建）
window.resize(500, 400)
window.move(300, 310)  # 移动程序（左上角）的位置
window.setWindowTitle('薪资统计')

# Qt中的控件是层层堆叠的，“window”的上级是电脑屏幕，所以移动位置是针对屏幕左上角位置而言的
# 而以下的移动位置，则是针对控件“QPlainTextEdit”的上级控件“window”的左上角位置（不包含标题栏）而言的
textEdit = QPlainTextEdit(window)
textEdit.setPlaceholderText("请输入薪资表")
textEdit.move(10, 25)
textEdit.resize(300, 350)

button = QPushButton('统计', window)
button.move(380, 80)
button.clicked.connect(MyMethod1)

window.show()

app.exec()  # 进入QApplication的事件处理循环，接收用户的输入事件（），并且分配给相应的对象去处理。
# PySide6 是 exec 而不是 exec_
#********************************* 至此创建了一个窗口，其中包含了一个按钮
