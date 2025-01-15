# 1 wx.Frame
# wx.Frame 类有一个没有参数的默认构造函数。
#
# 2	wx.Panel
# wx.Panel 类通常放在一个wxFrame 对象中。 这个类也是继承自wxWindow类。
#
# 3	wx.StaticText
# wx.StaticText 类对象提供了一个包含这种只读文本的控件。 它可以称为被动控件，因为它不产生任何事件。
#
# 4	TextCtrl
# 在wxPython 中，wx.TextCtrl 类的一个对象用于此目的。 它是一个可以在其中显示和编辑文本的控件。
#
# 5	RadioButton & RadioBox
# 每个按钮都是 wx.RadioButton 类的一个对象，在圆形按钮旁边带有一个文本标签。
# wxPython API 也由 wx.RadioBox 类组成。 它的对象为组提供了边框和标签。
#
# 6	wx.CheckBox
# 复选框显示一个带标签的小矩形框。单击时，矩形内会出现一个复选标记，表示已做出选择。
#
# 7	ComboBox & Choice Class
# 一个 wx.ComboBox 对象呈现一个项目列表以供选择。 它可以配置为下拉列表或永久显示。
# wxPython API包含一个wx.Choice类，它的对象也是一个下拉列表，它是永久只读的。
#
# 8	Wx.Gauge
# Wx.Gauge 类对象显示垂直或水平条，以图形方式显示递增的数量。
#
# 9	wx.Slider
# wxPython API 包含 wx.Slider 类。 它提供与滚动条相同的功能。 Slider 提供了一种方便的方法来通过滑块特定的 wx.EVT_SLIDER 事件绑定器来处理拖动句柄。
#
# 10	wx.MenuBar
# 顶层窗口标题栏正下方的水平条保留用于显示一系列菜单。 它是 wxPython API 中 wx.MenuBar 类的一个对象。
#
# 11	wx.Toolbar
# 如果wx.Toolbar对象的style参数设置为wx.TB_DOCKABLE，它就变成可停靠的。 还可以使用 wxPython 的 AUIToolBar 类构造浮动工具栏。
#
# 12	Wx.Dialog
# 虽然 Dialog 类对象看起来像一个框架，但它通常用作父框架顶部的弹出窗口。 对话框的目的是从用户那里收集一些数据并将其发送到父框架。
#
# 13	wx.Notebook
# wx.Notebook 小部件提供了一个选项卡式控件。 框架中的一个 Notebook 对象有一个或多个选项卡（称为页面），每个选项卡都有一个显示控件布局的面板。
#
# 14	wx.SplitterWindow
# 这个类的对象是一个布局管理器，它包含两个子窗口，其大小可以通过拖动它们之间的边界来动态改变。 Splitter 控件提供了一个可以拖动以调整控件大小的手柄。
#
# 15	HTMLWindow
# wxHTML 库包含用于解析和显示 HTML 内容的类。 虽然这不是一个全功能的浏览器，但 wx.HtmlWindow 对象是一个通用的 HTML 查看器。
#
# 16	ListBox & ListCtrl
# 一个 wx.ListBox 小部件呈现一个垂直滚动的字符串列表。 默认情况下，列表中的单个项目是可选择的。 ListCtrl 小部件是高度增强的列表显示和选择工具。 多列列表可以显示在报表视图、列表视图或图标视图中。

#