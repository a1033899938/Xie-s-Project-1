def foo(param1, *param2):
    print(param1)
    print(param2)


foo(1, 2, 3, 4, 5)  # *的形式参数，以元组（tuple）的形式导入


print("########")
def bar(param1, **param2):
    print(param1)
    print(param2)


bar(1, a=2, b=3)        # **的形式参数，以字典的形式导入


print("########")
def foo(runoob_1, runoob_2):
    print(runoob_1, runoob_2)
l = [1, 2]
foo(*l)     # 单星号的另一个用法是解压参数列表
