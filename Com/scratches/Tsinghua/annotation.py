"""
annotation.py
---------------  # 1 模块注释：描述模块的功能、作者信息和日期。
功能：这是一个示例模块，展示了如何使用文档注释、函数注释和类注释。
作者：Junjie Xie
创建日期：2024-09-27
最后修改日期：2024-09-27
"""
# 导入模块
import os
import json

# 该模块用于读取文件并将其转换为JSON格式


class DataProcessor:
    """
    数据处理类，用于清理和转换数据。  # 2 类注释：描述该类的用途，列出类的属性和方法。
    属性：
        raw_data (list): 未处理的数据
    方法：
        clean_data(): 清理数据
        transform_data(): 转换数据
    """

    def __init__(self, raw_data):
        """
        初始化数据处理器。  # 3 构造函数注释：说明初始化时传入的参数。
        参数：
            raw_data (list): 未处理的数据列表
        """
        self.raw_data = raw_data

    def clean_data(self):
        """
        清理数据，去除空值。  # 4 方法注释：说明方法的功能和返回值。
        返回：
            list: 清理后的数据列表  # 类型：简要说明返回值是什么
        """
        # 移除空值
        return [item for item in self.raw_data if item]


def export_to_json(data, save_path):
    """
    导出数据为JSON文件。  # 5 函数注释：描述函数的功能、输入参数和返回值。
    参数：
        data (list): 要导出的数据  # 参数名（类型）：简要说明输入参数是什么
        save_path (str): 保存JSON文件的路径
    返回：
        None
    """
    with open(save_path, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    # 测试DataProcessor类和export_to_json函数  # 7 代码块注释：说明代码的目的和作用。
    raw_data = ['Hello', 'WORLD', '', 'Python']
    processor = DataProcessor(raw_data)

    cleaned_data = processor.clean_data()
    print(f"清理后的数据: {cleaned_data}")

    transformed_data = processor.transform_data()
    print(f"转换后的数据: {transformed_data}")

    # 导出数据到JSON文件  # 8 代码块注释：描述导出操作和保存路径。
    export_path = 'processed_data.json'
    export_to_json(transformed_data, export_path)
    print(f"数据已导出到 {export_path}")

