# 与以顺序方式执行的控制台模式应用程序不同，基于 GUI 的应用程序是事件驱动的。
# 函数或方法是响应用户的操作而执行的
import wx


class Example(wx.Frame):  # 子类Example调用父类wx.Frame

    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)      # 从父类中调用方法__init__,并把*args和**kw作为参数
        self.InitUI()       # 调用自己（这个Example类的InitUI方法）

    def InitUI(self):
        self.Bind(wx.EVT_MOVE, self.OnMove)     # Bind()方法由wx.EvtHandler类的所有显示对象继承。作用是将事件（参数1）
        # 关联到方法（参数二）中
        self.SetSize(250, 180)
        self.SetTitle('Move Event')
        self.Center()
        self.Show(True)

    def OnMove(self, e):
        x, y = e.GetPosition()
        print("current window position x= ", x, " y= ", y)


ex = wx.App()       # 实例化
Example(None)
ex.MainLoop()


# GUI编程都有一个主体的死循环，一旦退出这个死循环，程序就结束了。
# mainloop就可以理解为这样一个循环，只是这个循环里面还有消息队列，其伪代码是：
# def mainloop():
# 	while the main window has not been closed:
# 		if an event has occurred:
# 			run the associated event handler function


