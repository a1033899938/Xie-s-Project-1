import wx


class MyPanel(wx.Panel):

    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        b = wx.Button(self, label='Btn', pos=(100, 100))
        b.Bind(wx.EVT_BUTTON, self.btnclk)      # 将事件wx.EVT_BUTTON与本类中的方法btnclk绑定
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)      # 将事件wx.EVT_BUTTON与本类中的方法OnButtonClicked绑定

    def OnButtonClicked(self, e):
        print('Panel received click event. propagated to Frame class', e.Skip())

    def btnclk(self, e):
        print("Button received click event. propagated to Panel class", e.Skip())


class Example(wx.Frame):

    def __init__(self, parent):
        super(Example, self).__init__(parent)

        self.InitUI()

    def InitUI(self):
        mpnl = MyPanel(self)            # 将Example类的self作为参数导入MyPanel,将Mypanel实例化
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)      # 将事件wx.EVT_BOTTON（点击按钮）与本类的方法OnButtonClicked绑定

        self.SetTitle('Event propagation demo')     # 设置UI窗口标题
        self.Centre()
        self.Show(True)

    def OnButtonClicked(self, e):
        print('click event received by frame class', e.Skip())


ex = wx.App()
Example(None)
ex.MainLoop()