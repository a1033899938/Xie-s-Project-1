from PIL import Image
import pytesseract
import pandas as pd

# 设置tesseract的路径（根据你的安装路径进行修改）
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'

# 打开图片
image_path = r'C:\Users\a1033\Pictures\Acer\pic1.png'  # 替换为你的图片路径
image = Image.open(image_path)

# 识别图片中的中文文本
text = pytesseract.image_to_string(image, lang='chi_sim')  # 使用简体中文

# 将文本处理为行列表
lines = text.splitlines()

# 创建DataFrame
df = pd.DataFrame(lines, columns=['识别文本'])

# 保存为Excel文件
output_path = 'output.xlsx'  # 替换为你想要的输出文件名
df.to_excel(output_path, index=False)

print("识别完成，结果已保存为Excel文件。")
