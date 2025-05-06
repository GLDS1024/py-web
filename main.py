import streamlit as st
import pandas as pd
import openpyxl
import io
import os
import base64
import platform
from pathlib import Path

st.set_page_config(page_title="Excel 검색", layout="wide")

# 1. 加载 Excel
if platform.system() == "Windows":
    excel_path = os.path.join(os.environ['USERPROFILE'], "Downloads") + "/메모장.xlsx"
else:
    excel_path = os.path.join(Path.home(), "Downloads") + "/메모장.xlsx"

if not os.path.exists(excel_path):
    st.error("❌ 메모장.xlsx 없슴니다~ ")
    st.stop()


# 2. 读取文字表格
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

# 4. 用户输入关键词 & 颜色
keyword = st.text_input("검색：")
color   = st.color_picker("검색단어색상", "#ff0000")

# 5. 先筛出匹配行
if keyword:
    mask = df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)
    matched_df = df[mask]
    if matched_df.empty:
        st.warning("⚠️ 일치하는 항목이 없습니다。")
        st.stop()
else:
    matched_df = df

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
            f"<span style='color:{color}; font-weight:bold;'>{keyword}</span>"
        )
    return s

# 7. 构建仅含匹配行的 HTML 表格
cols = matched_df.columns.tolist()
style = """
<style>
table {border-collapse: collapse; width: 100%; font-size: 14px;}
th { background-color: #333; color: #fff;padding: 2px; text-align: left;}
td { border-bottom: 1px solid #ddd; padding: 2px; white-space: pre-wrap;}
th:nth-child(1), td:nth-child(1) { width: 80px; text-align: center; }
</style>
"""

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

# 8. 渲染结果
st.success(f"✅ 총 {len(matched_df)} 라인 매칭：")
st.markdown(style + html, unsafe_allow_html=True)
