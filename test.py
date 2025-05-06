import pandas as pd
import openpyxl
import io
import os
import base64
import platform
from pathlib import Path

# 1. 加载 Excel
if platform.system() == "Windows":
    excel_path = os.path.join(os.environ['USERPROFILE'], "Downloads") + "/메모장.xlsx"
else:
    excel_path = os.path.join(Path.home(), "Downloads") + "/메모장.xlsx"

if not os.path.exists(excel_path):
    print("❌ 메모장.xlsx 없슴니다~ ")

df = pd.read_excel(excel_path)

# 3. 读取嵌入图片并映射 (row, col) -> bytes
wb = openpyxl.load_workbook(excel_path)
ws = wb.active
img_map = {}
for img in ws._images:
    a = img.anchor._from
    key = (a.row + 1, a.col + 1)
    raw = img._data()
    if isinstance(raw, bytes):
        img_bytes = raw
    else:
        buf = io.BytesIO()
        raw.save(buf, format="PNG")
        img_bytes = buf.getvalue()
    img_map[key] = img_bytes

matched_df = df

cols = matched_df.columns.tolist()
style = """
<style>
table {border-collapse: collapse; width: 100%; font-size: 14px;}
th { background-color: #333; color: #fff;padding: 2px; text-align: left;}
td { border-bottom: 1px solid #ddd; padding: 2px; white-space: pre-wrap;}
th:nth-child(1), td:nth-child(1) { width: 80px; text-align: center; }
</style>
"""

keyword='afsd'
# 6. 文本高亮函数 —— 隐藏 NaN、保留换行、关键词变色
def highlight_text(val):
    # 先处理 NaN
    if pd.isna(val):
        return ""
    s = str(val) #.replace("\n", "<br>")
    # 高亮关键词
    if keyword.lower() in s.lower():
        return s.replace(
            keyword,
            f"<span style='color:red; font-weight:bold;'>{keyword}</span>"
        )
    return s

html = "<table><thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead><tbody>"
for idx, row in matched_df.iterrows():
    excel_row = idx + 2  # DataFrame 行 idx 对应 Excel 行
    html += "<tr>"
    for j, col in enumerate(cols):
        cell_key = (excel_row, j+1)
        if cell_key in img_map:
            b64 = base64.b64encode(img_map[cell_key]).decode('utf-8')
            html += f"<td><img src='data:image/png;base64,{b64}'/></td>"
        else:
            html += f"<td>{highlight_text(row[col])}</td>"
    html += "</tr>"
html += "</tbody></table>"

print(html)