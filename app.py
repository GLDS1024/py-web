import streamlit as st
import pandas as pd

# 设置页面为宽屏模式
st.set_page_config(layout="wide")

st.title("🔍 Excel 查找工具")

# 上传 Excel 文件
uploaded_file = st.file_uploader("上传 Excel 文件", type=["xlsx"])

if uploaded_file:
    # 读取 Excel 文件为 DataFrame
    df = pd.read_excel(uploaded_file)
    st.success("文件上传成功，读取了 {} 行 {} 列。".format(*df.shape))

    # 显示预览
    with st.expander("📄 查看前几行数据"):
        st.dataframe(df)

    # 输入查询关键字
    query = st.text_input("请输入要查找的内容（模糊匹配）")

    if query:
        # 转换为字符串并查找包含关键词的行（逐列匹配）
        mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
        result = df[mask]

        # 显示结果
        st.write(f"🔎 共找到 {len(result)} 行匹配 “{query}”：")
        st.dataframe(result)

        # 可选：下载结果
        if not result.empty:
            csv = result.to_csv(index=False).encode("utf-8-sig")
            st.download_button("📥 下载结果为 CSV", csv, file_name="search_result.csv")
else:
    st.info("请上传 Excel 文件以开始。")