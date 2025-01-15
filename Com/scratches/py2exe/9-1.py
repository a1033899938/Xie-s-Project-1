# .py  to .exe过程
# 在终端中进行以下操作
# 0. 创建并进入这个可执行文件的文件夹   # 如果进不去尝试在cd后加入/d，如：“cd /d d”q:
# 1. pip install pipenv    # 安装虚拟环境pipenv
# 2. pipnev shell  # 进入虚拟环境，此时路径前面应该多了一个圆括号，里面是虚拟环境名称
# 3. pipenv install pyinstaller     # 在虚拟环境中安装pyinstaller
# 4. pipenv install xxx     # 在虚拟环境中安装我们脚本依赖的所有库，此时用pip list应该发现，里面只有很少的库
# 5. 将所有程序复制到这个文件夹下
# 6-1. pyinstaller -F xx.py   #最简单的，只打包一个程序
# 6-2. pyinstaller -F -w -i yy.ico xx.py      # 打包一个程序，并且exe运行时不显示控制台（-w），加入exe图标（-i）
# 6-3. pyinstaller -F xx.py -p pyfolder        # 打包多个程度，xx.py为主程序，pyfolder为附属程序所在文件夹名
# 转换结束后，有时pipenv无法删除库，用pipenv uninstall删除命令后包还在。此时直接删除虚拟环境可以解决。


# 如何将资源文件一起打包？
# 一般的引用方式是通过相对路径引用，而打包成exe文件就只能在这个项目的文件夹里使用。
# 如果我们给程序中的资源加入绝对路径呢？exe文件可以在这台电脑的任何地方使用，但是分享给别人，换一台电脑，路径变了就不能使用了。
# 所以我们需要更改读取资源的方式：
# 基本原理：
# Pyinstaller 可以将资源文件一起bundle到exe中。
# 当exe在运行时，会生成一个临时文件夹，程序可通过sys._MEIPASS访问临时文件夹中的资源。
# 0. 与上述方式相同，先安装虚拟环境和程序依赖的库
# 1. 将.py和存放资源的folder放在同一个根目录下
# 2. 修改.py文件中的读取资源的代码
#


# pyinstaller常见命令：
# -i：给应用程序添加图标
# -F：指定打包后只生成一个exe格式的文件
# -D –onedir：创建一个目录，包含exe文件，但会依赖很多文件（默认选项）
# -c –console, –nowindowed：使用控制台，无界面(默认)
# -w –windowed, –noconsole：使用窗口，无控制台
# -p：添加搜索路径


# pipenv常见命令：
# pipenv install ：创建虚拟环境
# pipenv shell ：进入虚拟环境（如果不存在，则创建并进入虚拟环境）
# pipenv install flask： 安装模块
# pipenv uninstall flask ：卸载模块
# pipenv graph：查看模块之间的依赖关系
# pip list：查看虚拟环境所有模块
# exit() ：退出虚拟环境
# pip freeze > requirements.txt：导出虚拟环境所有依赖包名
# pip install -r requirements.txt ：安装项目所依赖全部模块
# pipenv uninstall --all ：卸载所有包
# pipenv lock：生成lockfile
# pipenv --rm： 删除虚拟环境
# pipenv run python xxx.py： 虚拟环境运行python
