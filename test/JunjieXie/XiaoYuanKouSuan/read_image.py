import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'


def preprocess_image(img_path):
    """
    使用 OpenCV 对图像进行预处理以提高 OCR 识别准确率。
    """
    # 读取图像
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # 对图像进行二值化处理
    _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 反转二值图像（因为Tesseract处理白色背景和黑色文字效果更好）
    img_bin = cv2.bitwise_not(img_bin)

    return img_bin


def recognize_digits(img_path):
    """
    识别图像中的数字。
    """
    # 预处理图像
    processed_img = preprocess_image(img_path)

    # 配置 Tesseract 只识别数字
    custom_config = r'--oem 3 --psm 6 outputbase digits'

    # 使用 pytesseract 识别图像中的数字
    recognized_text = pytesseract.image_to_string(processed_img, config=custom_config)

    return recognized_text.strip()


if __name__ == "__main__":
    img_path = r'D:\GitProject\SpectraPro\test\JunjieXie\XiaoYuanKouSuan\pic3.jpg'

    import time

    # 记录识别开始时间
    start_time = time.time()

    # 识别数字
    digits = recognize_digits(img_path)

    # 记录识别结束时间
    end_time = time.time()

    # 输出结果和识别耗时
    print(f"识别到的数字: {digits}")
    print(f"识别耗时: {end_time - start_time:.4f} 秒")
