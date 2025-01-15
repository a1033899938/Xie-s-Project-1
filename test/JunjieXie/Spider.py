import pandas as pd
from scholarly import scholarly
from Bio import Entrez
import time

# 设置 Entrez 电子邮件，确保可以访问 PubMed 数据库
Entrez.email = "your_email@example.com"  # 这里填入你的电子邮箱地址


def search_scholar(query):
    # 搜索输入字段
    print(f"正在搜索: {query}")
    search_query = scholarly.search_pubs(query)

    results = []
    try:
        for i, result in enumerate(search_query):
            if i >= 10:  # 限制返回10条结果，避免过多请求
                break

            # 直接从字典中提取信息
            title = result.get('bib', {}).get('title', 'N/A')
            authors = ', '.join(result.get('bib', {}).get('author', []))
            pub_year = result.get('bib', {}).get('pub_year', 'N/A')
            venue = result.get('bib', {}).get('venue', 'N/A')
            citation_count = result.get('num_citations', 'N/A')
            pub_type = result.get('bib', {}).get('ENTRYTYPE', 'N/A')
            download_link = result.get('eprint_url', 'N/A')  # 获取文章下载链接
            doi = get_doi_from_pubmed(title)  # 调用 PubMed 搜索获取 DOI

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


def get_doi_from_pubmed(title):
    """
    使用 PubMed API 根据文章标题搜索并返回 DOI
    """
    try:
        handle = Entrez.esearch(db="pubmed", term=title, retmode="xml")
        record = Entrez.read(handle)
        handle.close()
        if record['IdList']:
            pubmed_id = record['IdList'][0]
            handle = Entrez.efetch(db="pubmed", id=pubmed_id, retmode="xml")
            records = Entrez.read(handle)
            handle.close()

            # 遍历返回结果，查找 DOI
            for article in records["PubmedArticle"]:
                if "ELocationID" in article["MedlineCitation"]["Article"]:
                    for loc in article["MedlineCitation"]["Article"]["ELocationID"]:
                        if loc.attributes.get('EIdType') == 'doi':
                            return loc
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


if __name__ == '__main__':
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
        filename = f"{'mmy20241023'}_scholar_results.xlsx"
        save_to_excel(results, filename)
