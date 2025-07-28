import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.markdown(
    """
    <style>
    .centered-login {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 80vh;
    }
    .login-title {
        font-size: 1.2em;
        font-weight: 500;
        margin-bottom: 0.2em;
        margin-top: 1em;
    }
    .login-subtitle {
        font-size: 1em;
        color: #666;
        margin-bottom: 2em;
    }
    .login-btn {
        width: 100%%;
        padding: 0.9em;
        font-size: 1.1em;
        font-weight: bold;
        margin-bottom: 1em;
        border-radius: 8px;
    }
    </style>
    <div class="centered-login">
        <div class="login-title">Chào mừng ba/mẹ trở lại!</div>
        <div class="login-subtitle">Cùng con tiếp tục hành trình nhé</div>
    </div>
    """,
    unsafe_allow_html=True,
)

phone = st.text_input("Nhập số điện thoại:", key="login_phone", label_visibility="collapsed")

col1, col2 = st.columns(2)
with col1:
    if st.button("Đăng nhập"):
        st.success(f"Đăng nhập với số điện thoại: {phone}")
with col2:
    if st.button("Tạo tài khoản"):
        st.info(f"Tạo tài khoản với số điện thoại: {phone}")