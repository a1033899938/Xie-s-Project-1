import pyautogui


class DrawSign:
    def __init__(self, position):
        self.draw_position = position  # 起始绘制位置
        self.size = 50  # 控制绘制符号的大小

    def draw_something(self, symbol_type):
        """
        根据符号类型选择绘制内容：
        1 -> 大于号
        2 -> 小于号
        3 -> 等号
        """
        if symbol_type == 1:
            self.draw_greater_than_symbol()
        elif symbol_type == 2:
            self.draw_less_than_symbol()
        elif symbol_type == 3:
            self.draw_equal_symbol()

    def draw_greater_than_symbol(self):
        """绘制大于号 '>' """
        # 移动到大于号的起点位置（左上角）
        pyautogui.moveTo(self.draw_position[0], self.draw_position[1])
        pyautogui.mouseDown()
        pyautogui.moveRel(self.size, self.size, duration=0.05)  # 画大于号的上半部分
        pyautogui.mouseUp()

        # 移动到第二段起始位置
        pyautogui.moveTo(self.draw_position[0], self.draw_position[1] + self.size)
        pyautogui.mouseDown()
        pyautogui.moveRel(self.size, -self.size, duration=0.05)  # 画大于号的下半部分
        pyautogui.mouseUp()

    def draw_less_than_symbol(self):
        """绘制小于号 '<' """
        # 移动到小于号的起点位置（右上角）
        pyautogui.moveTo(self.draw_position[0] + self.size, self.draw_position[1])
        pyautogui.mouseDown()
        pyautogui.moveRel(-self.size, self.size, duration=0.05)  # 画小于号的上半部分
        pyautogui.mouseUp()

        # 移动到第二段起始位置
        pyautogui.moveTo(self.draw_position[0] + self.size, self.draw_position[1] + self.size)
        pyautogui.mouseDown()
        pyautogui.moveRel(-self.size, -self.size, duration=0.05)  # 画小于号的下半部分
        pyautogui.mouseUp()

    def draw_equal_symbol(self):
        """绘制等号 '=' """
        # 第一条横线
        pyautogui.moveTo(self.draw_position[0], self.draw_position[1])
        pyautogui.mouseDown()
        pyautogui.moveRel(self.size, 0, duration=0.05)  # 画第一条线
        pyautogui.mouseUp()

        # 移动到第二条横线的位置
        pyautogui.moveTo(self.draw_position[0], self.draw_position[1] + self.size * 0.5)
        pyautogui.mouseDown()
        pyautogui.moveRel(self.size, 0, duration=0.05)  # 画第二条线
        pyautogui.mouseUp()


if __name__ == '__main__':

    drawSign = DrawSign([1919, 1240])  # 起始绘制位置
    drawSign.draw_something(1)  # 绘制大于号
    drawSign.draw_something(2)  # 绘制小于号
    drawSign.draw_something(3)  # 绘制等号
