import os
import fitz  # PyMuPDF
import re

# 定义一个函数，根据PDF类型提取指定位置的文本内容
def extract_text_from_pdf(pdf_path, pdf_type):
    document = fitz.open(pdf_path)
    text = ''
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()

    if pdf_type == '放款凭证':
        pattern = r"借款人姓名：([\u4e00-\u9fa5]+)"
        match = re.search(pattern, text)
     #   match = re.search(r'借款人姓名:', text)
        if match:
            return match.group(1)
        else:
            return '1'
    elif pdf_type == '代偿凭证':
        pattern = r"借款人([\u4e00-\u9fa5]+)\(身份证号码"
        match = re.search(pattern, text)
      #  match = re.search(r'借款人(.*?)（身份证号码', text)
        if match:
            return match.group(1)
        else:
            return '1'
    elif pdf_type == '借款合同':
        match = re.search(r'借款人：([\u4e00-\u9fa5]+)', text)
        if match:
            return match.group(1)
        else:
            return '1'
    else:
        return '读不到文件'

new_pdf_path = r'D:\py\data\pdf_name\new_pdf\123'

# 遍历文件夹
for root, dirs, files in os.walk(r'D:\py\data\pdf_name\pdf'):
    for file in files:
        if file.endswith('.pdf'):
            pdf_path = os.path.join(root, file)
            pdf_type = '放款凭证' if '放款凭证' in file else '借款合同' if '借款合同' in file else '代偿凭证'
            name = extract_text_from_pdf(pdf_path, pdf_type)
            new_pdf_name = os.path.join(root, file.split('.pdf')[0] + name + '.pdf')
            # new_pdf_name = os.path.join(new_pdf_path, file.split('.pdf')[0] + name + '.pdf')  # 测试使用
            os.rename(pdf_path, new_pdf_name)

