def test():# 定义方法（类似matlab中的函数）
    try:
        a = 5.0 / 0.0# 除数为0，代码异常，执行except段代码
        print("I'm try")
        return 0
    except:
        print("I'm except")
        return 1# 返回值为1，执行finally段代码
    else:
        print("I'm else")
        return 2
    finally:
        print("I'm finally")
        return 3# 返回值为3，覆盖了之前的返回值1
print('test: ',test())