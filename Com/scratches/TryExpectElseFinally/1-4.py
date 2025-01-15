def test():
    try:
        a = 5.0 / 1.0# 除数为1，代码正常
        print("I'm try")# 未返回值，执行else段代码    except:
        print("I'm except")
        return 0
    except:
        print("I'm except")
        return 1
    else:
        print("I'm else")
        return 2# 返回值2

    finally:
        print("I'm finally")
print('test: ',test())