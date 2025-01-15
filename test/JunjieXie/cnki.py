import pandas as pd
from scholarly import scholarly
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import time


def search_scholar(query):
    # 搜索输入字段
    print(f"正在搜索: {query}")
    N = int(input("搜索文献数:"))
    search_query = scholarly.search_pubs(query)
    results = []
    try:
        for i, result in enumerate(search_query):
            if i >= N+1:  # 限制返回10条结果，避免过多请求
                break

            # 直接从字典中提取信息
            title = result.get('bib', {}).get('title', 'N/A')
            authors = ', '.join(result.get('bib', {}).get('author', []))
            pub_year = result.get('bib', {}).get('pub_year', 'N/A')
            venue = result.get('bib', {}).get('venue', 'N/A')
            citation_count = result.get('num_citations', 'N/A')
            pub_type = result.get('bib', {}).get('ENTRYTYPE', 'N/A')
            download_link = result.get('eprint_url', 'N/A')  # 获取文章下载链接
            doi = get_doi_from_crossref(title)  # 调用 CrossRef API 获取 DOI

            results.append({
                '标题': title,
                '类型': pub_type,
                '期刊': venue,
                '作者': authors,
                '年份': pub_year,
                '被引次数': citation_count,
                '下载链接': download_link,
                'DOI': doi
            })

            if i // 10 == 0:
                time.sleep(2)

        return results
    except Exception as e:
        print(f"检索出现问题: {e}")
        return results


def get_doi_from_crossref(title):
    """
    使用 CrossRef API 根据文章标题搜索并返回 DOI
    """
    url = "https://api.crossref.org/works"
    params = {
        "query.title": title,
        "rows": 1  # 只获取一个最相关的结果
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果请求失败则抛出异常
        data = response.json()
        if "items" in data["message"] and len(data["message"]["items"]) > 0:
            doi = data["message"]["items"][0].get("DOI", "N/A")
            return doi
    except Exception as e:
        print(f"获取 DOI 失败: {e}")
        return "N/A"

    return "N/A"


def save_to_excel(data, filename):
    # 使用 pandas 将数据转换为 DataFrame
    df = pd.DataFrame(data)

    # 将数据保存为 Excel 文件
    df.to_excel(filename, index=False)
    print(f"数据已保存为 {filename}")


def download_paper_as_chrome_selenium(doi, output_folder="downloads"):
    """
    使用 Selenium 启动 Chrome 浏览器下载 PDF 文件。
    """

    print(f"Dealing with {doi}")

    tesble_url = f"https://www.tesble.com/{doi}"
    service = Service('C:\\Windows\\System32\\chromedriver.exe')  # 替换为 ChromeDriver 的实际路径
    options = webdriver.ChromeOptions()

    # 设置 Chrome 下载选项
    prefs = {
        "download.default_directory": os.path.abspath(output_folder),  # 设置默认下载路径
        "download.prompt_for_download": False,  # 不弹出下载窗口
        "safebrowsing.enabled": True  # 允许自动下载
    }
    options.add_experimental_option("prefs", prefs)

    # 其他 Chrome 选项
    options.add_argument("--headless")  # 如果想隐藏浏览器窗口，可以启用此选项
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(service=service, options=options)

    # 创建下载目录（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        # 打开目标网址
        driver.get(tesble_url)
        time.sleep(5)  # 等待页面加载

        # 查找页面中 PDF 的下载按钮
        download_button = driver.find_element(By.TAG_NAME, 'a')  # 需要根据实际页面调整选择器
        pdf_url = download_button.get_attribute('href')

        if pdf_url:
            # 点击下载链接
            driver.get(pdf_url)

            # 等待文件下载完成
            if wait_for_download_complete(output_folder):
                print(f"文献下载成功: {doi}.")
            else:
                print(f"下载 {doi} 失败：文件下载超时或未完成。")
        else:
            print(f"未能找到 DOI {doi} 对应的 PDF 下载链接。")

    except Exception as e:
        print(f"下载失败: {doi}. 错误信息: {e}")

    finally:
        driver.quit()


def read_doi_from_excel_and_download(excel_path, output_folder="downloads"):
    """
    读取 Excel 文件的第 H 列中的 DOI 并从 tesble.com 下载。
    """
    try:
        # 读取 Excel 文件
        df = pd.read_excel(excel_path, usecols="H")

        # 遍历 DOI 列并下载文献
        for doi in df.iloc[:, 0].dropna():
            download_paper_as_chrome_selenium(str(doi).strip(), output_folder=output_folder)

    except Exception as e:
        print(f"读取 Excel 文件失败: {e}")


def wait_for_download_complete(download_dir, check_interval=1, timeout=300):
    """
    等待文件下载完成，通过检测下载目录中的临时文件。
    """
    start_time = time.time()
    download_complete = False

    while time.time() - start_time < timeout:
        # 检查下载目录中是否有文件正在下载（临时文件）
        downloading_files = [
            f for f in os.listdir(download_dir)
            if f.endswith('.crdownload') or f.endswith('.tmp') or f.endswith('.part')
        ]

        # 如果没有发现临时文件，则认为下载完成
        if not downloading_files:
            download_complete = True
            break

        time.sleep(check_interval)

    return download_complete


if __name__ == '__main__':
    """搜索文献"""
    # 输入搜索字段
    query = input("请输入搜索字段: ")
    results = search_scholar(query)
    print(results)
    # 输出结果
    for result in results:
        print(f"标题: {result['标题']}")
        print(f"类型: {result['类型']}")
        print(f"期刊: {result['期刊']}")
        print(f"作者: {result['作者']}")
        print(f"年份: {result['年份']}")
        print(f"被引次数: {result['被引次数']}")
        print(f"下载链接: {result['下载链接']}")
        print(f"DOI: {result['DOI']}")
        print("=" * 40)

    # 如果有结果，保存为 Excel 文件
    if results:
        filename = f"{'xie20241023'}_scholar_results.xlsx"
        save_to_excel(results, filename)

    # """下载文献"""
    # excel_path = "mmy20241023_scholar_results.xlsx"  # 替换为实际的 Excel 文件路径
    # read_doi_from_excel_and_download(excel_path)
