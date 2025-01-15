try:# 正常情况下执行
    # 代码1
    a = 5.0 / 0.0
    print("I'm try")
except:# try段代码异常时执行
    # 代码2
    print("I'm except")
else:# try段代码无异常时，执行完try段代码后执行
    # 代码3
    print("I'm else")
finally:# 无论有无异常，都会执行
    # 代码4
    print("I'm finally")


# 临时文件1练习了try except else finally的用法
