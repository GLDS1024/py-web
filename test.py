import streamlit as st
import time

st.title("进度条示例")
progress = st.progress(0)

for i in range(100):
    time.sleep(0.05)
    progress.progress(i + 1)

st.success("加载完成！")