
import streamlit as st
import requests

API_URL = "http://localhost:8000"

if "step" not in st.session_state:
    st.session_state.step = "login"
if "customer_id" not in st.session_state:
    st.session_state.customer_id = None
if "children" not in st.session_state:
    st.session_state.children = []
if "phone" not in st.session_state:
    st.session_state.phone = ""

def go_to(step):
    st.session_state.step = step

# Step 1: Đăng nhập/Đăng ký bằng số điện thoại
if st.session_state.step == "login":
    st.header("Đăng nhập / Đăng ký")
    phone = st.text_input("Số điện thoại", value=st.session_state.phone)
    if st.button("Tiếp tục"):
        st.session_state.phone = phone
        resp = requests.get(f"{API_URL}/customers/phone/{phone}")
        if resp.status_code == 200:
            st.success("Số điện thoại đã tồn tại. Đăng nhập thành công!")
            st.session_state.customer_id = resp.json().get("id") or resp.json().get("user_id")
            go_to("add_children")
        else:
            st.info("Số điện thoại chưa tồn tại. Đăng ký mới!")
            go_to("register")

# Step 2: Đăng ký tên nếu là user mới
if st.session_state.step == "register":
    st.header("Đăng ký tài khoản mới")
    phone = st.text_input("Số điện thoại", value=st.session_state.phone, disabled=True, key="register_phone")
    name = st.text_input("Tên khách hàng", key="register_name")
    if st.button("Đăng ký"):
        payload = {"phone": phone, "name": name}
        resp = requests.post(f"{API_URL}/customers/", json=payload)
        if resp.status_code == 200:
            st.success("Đăng ký thành công!")
            st.session_state.customer_id = resp.json().get("id") or resp.json().get("user_id")
            go_to("add_children")
        else:
            detail = resp.json().get("detail", "Lỗi đăng ký")
            # Nếu đã tồn tại thì chuyển sang bước tạo con luôn
            if "already registered" in detail or "đã tồn tại" in detail:
                get_resp = requests.get(f"{API_URL}/customers/phone/{phone}")
                if get_resp.status_code == 200:
                    st.session_state.customer_id = get_resp.json().get("id") or get_resp.json().get("user_id")
                    st.success("Số điện thoại đã tồn tại. Đăng nhập thành công!")
                    go_to("add_children")
                else:
                    st.error("Không lấy được thông tin khách hàng!")
            else:
                st.error(detail)

# Step 3: Tạo con cái
if st.session_state.step == "add_children":
    st.header("Tạo con cái")
    # Lấy danh sách con từ API nếu chưa có
    if not st.session_state.children:
        resp = requests.get(f"{API_URL}/children/{st.session_state.customer_id}")
        if resp.status_code == 200:
            st.session_state.children = resp.json() if isinstance(resp.json(), list) else [resp.json()]
    children = st.session_state.children
    new_child_name = st.text_input("Tên con mới", key="new_child_name")
    if st.button("Thêm con") and new_child_name:
        payload = {"parent_id": st.session_state.customer_id, "name": new_child_name}
        resp = requests.post(f"{API_URL}/children/", json=payload)
        if resp.status_code == 200:
            children.append(resp.json())
            st.success(f"Đã thêm con: {new_child_name}")
            st.session_state.children = children
        else:
            try:
                detail = resp.json().get("detail", "Lỗi thêm con")
            except Exception:
                detail = f"Lỗi thêm con: {resp.text} (status {resp.status_code})"
            st.error(detail)
    st.write("Danh sách con đã tạo:")
    for c in children:
        st.write(f"- {c['name']}")
    if st.button("Hoàn thành tạo con"):
        go_to("add_money")

# Step 4: Nạp tiền vào tài khoản từng con
if st.session_state.step == "add_money":
    st.header("Nạp tiền vào tài khoản từng con")
    for child in st.session_state.children:
        st.subheader(f"Con: {child['name']}")
        child_id = child.get("id") or child.get("child_id")
        total = st.number_input(f"Số tiền nạp cho {child['name']}", min_value=0.0, format="%.2f", key=f"total_{child_id}")
        if st.button(f"Nạp tiền cho {child['name']}", key=f"btn_add_{child_id}"):
            resp = requests.post(f"{API_URL}/wallets/{child_id}/add-money", json={"total": total})
            if resp.status_code == 200:
                st.success(f"Đã nạp {total} cho {child['name']}")
            else:
                try:
                    detail = resp.json().get("detail", "Lỗi nạp tiền")
                except Exception:
                    detail = f"Lỗi nạp tiền: {resp.text} (status {resp.status_code})"
                st.error(detail)
    if st.button("Tiếp tục chia tiền"):
        go_to("split_money")

# Step 5: Chia tiền vào các ví con
if st.session_state.step == "split_money":
    st.header("Chia tiền vào các ví con")
    for child in st.session_state.children:
        st.subheader(f"Con: {child['name']}")
        child_id = child.get("id") or child.get("child_id")
        savings = st.number_input(f"Savings của {child['name']}", min_value=0.0, format="%.2f", key=f"savings_{child_id}")
        charity = st.number_input(f"Charity của {child['name']}", min_value=0.0, format="%.2f", key=f"charity_{child_id}")
        spending = st.number_input(f"Spending của {child['name']}", min_value=0.0, format="%.2f", key=f"spending_{child_id}")
        study = st.number_input(f"Study của {child['name']}", min_value=0.0, format="%.2f", key=f"study_{child_id}")
        if st.button(f"Chia tiền cho {child['name']}", key=f"btn_split_{child_id}"):
            payload = {
                "savings": savings if savings > 0 else None,
                "charity": charity if charity > 0 else None,
                "spending": spending if spending > 0 else None,
                "study": study if study > 0 else None
            }
            resp = requests.post(f"{API_URL}/wallets/{child_id}/split-money", json=payload)
            if resp.status_code == 200:
                st.success(f"Đã chia tiền cho {child['name']}")
            else:
                try:
                    detail = resp.json().get("detail", "Lỗi chia tiền")
                except Exception:
                    detail = f"Lỗi chia tiền: {resp.text} (status {resp.status_code})"
                st.error(detail)
    if st.button("Tiếp tục tiêu tiền"):
        go_to("spend_money")
    if st.button("Quay lại nạp tiền"):
        go_to("add_money")

# Step 6: Tiêu tiền
if st.session_state.step == "spend_money":
    st.header("Tiêu tiền từ ví con")
    for child in st.session_state.children:
        st.subheader(f"Con: {child['name']}")
        child_id = child.get("id") or child.get("child_id")
        amount = st.number_input(f"Số tiền chi của {child['name']}", min_value=0.0, format="%.2f", key=f"spend_amount_{child_id}" )
        wallet_type = st.selectbox(f"Loại ví của {child['name']}", ["spending", "savings", "charity", "study"], key=f"spend_type_{child_id}" )
        if st.button(f"Chi tiêu cho {child['name']}", key=f"btn_spend_{child_id}"):
            payload = {"amount": amount, "wallet_type": wallet_type}
            resp = requests.post(f"{API_URL}/wallets/{child_id}/spend", json=payload)
            if resp.status_code == 200:
                st.success(f"Đã chi {amount} từ ví {wallet_type} cho {child['name']}")
            else:
                try:
                    detail = resp.json().get("detail", "Lỗi chi tiêu")
                except Exception:
                    detail = f"Lỗi chi tiêu: {resp.text} (status {resp.status_code})"
                st.error(detail)
    if st.button("Quay lại chia tiền"):
        go_to("split_money")