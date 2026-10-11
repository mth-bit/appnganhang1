import streamlit as st
import pandas as pd
from database import save_request, get_all_requests
from datetime import datetime
import random

# =========================
# CẤU HÌNH ỨNG DỤNG
# =========================
st.set_page_config(
    page_title="DemoBank - Ngân hàng số",
    page_icon="🏦",
    layout="wide"
)

# Giao diện
st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
}
.main-title {
    background: linear-gradient(120deg, #073b8c, #0878d1);
    padding: 28px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
.service-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e0e8f2;
}
div.stButton > button {
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# KHỞI TẠO DỮ LIỆU
# =========================
if "requests" not in st.session_state:
    st.session_state.requests = []

if "accounts" not in st.session_state:
    st.session_state.accounts = []

if "cards" not in st.session_state:
    st.session_state.cards = []

if "savings" not in st.session_state:
    st.session_state.savings = []

if "loans" not in st.session_state:
    st.session_state.loans = []

# =========================
# TIÊU ĐỀ
# =========================
st.markdown("""
<div class="main-title">
    <h1>🏦 DemoBANK</h1>
    <h3>Ngân hàng số - Giao dịch dễ dàng</h3>
    <p>An toàn • Nhanh chóng • Tiện lợi</p>
</div>
# Thanh menu
menu = st.sidebar.radio(
    "📌 DANH MỤC DỊCH VỤ",
    [
        "🏠 Trang chủ",
        "💳 Mở thẻ ngân hàng",
        "👤 Mở tài khoản",
        "💰 Gửi tiết kiệm",
        "🏦 Vay vốn ngân hàng",
        "📋 Quản lý đăng ký"
    ]
)

st.sidebar.divider()
st.sidebar.info(
    "DemoBank\n\n"
    "Ứng dụng mô phỏng phục vụ học tập.\n"
    "Không thực hiện giao dịch tài chính thật."
)

# =========================
# HÀM LƯU YÊU CẦU
# =========================
def save_request(service, customer, details):
    request = {
        "Mã yêu cầu": "TB" + str(random.randint(100000, 999999)),
        "Dịch vụ": service,
        "Họ và tên": customer,
        "Thông tin": details,
        "Ngày đăng ký": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Trạng thái": "Chờ xử lý"
    }
    st.session_state.requests.append(request)
    return request["Mã yêu cầu"]


# =========================
# TRANG CHỦ
# =========================
if menu == "🏠 Trang chủ":

    st.subheader("Xin chào! Chào mừng đến với DemoBank 👋")
    st.write(
        "Khám phá các dịch vụ ngân hàng trực tuyến "
        "và gửi yêu cầu đăng ký ngay trên ứng dụng."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="bank-header">
        <h3>💳 Mở thẻ ngân hàng</h3>
        <p>Đăng ký thẻ ghi nợ hoặc thẻ tín dụng.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="service-card">
        <h3>👤 Mở tài khoản</h3>
        <p>Đăng ký tài khoản ngân hàng trực tuyến.</p>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="service-card">
        <h3>💰 Gửi tiết kiệm</h3>
        <p>Tìm hiểu tiền gửi và ước tính tiền lãi.</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="service-card">
        <h3>🏦 Vay vốn ngân hàng</h3>
        <p>Đăng ký nhu cầu vay vốn để được tư vấn.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("📊 Tổng quan đăng ký")

    c1, c2, c3 = st.columns(3)

    c1.metric("Tổng yêu cầu", len(st.session_state.requests))
    c2.metric("Tài khoản đăng ký", len(st.session_state.accounts))
    c3.metric("Yêu cầu vay vốn", len(st.session_state.loans))

    st.info("👉 Chọn một dịch vụ ở thanh menu bên trái để bắt đầu.")


# =========================
# 1. MỞ THẺ NGÂN HÀNG
# =========================
elif menu == "💳 Mở thẻ ngân hàng":

    st.subheader("💳 ĐĂNG KÝ MỞ THẺ NGÂN HÀNG")
    st.write("Điền thông tin để gửi yêu cầu đăng ký thẻ.")

    with st.form("card_form"):

        name = st.text_input("Họ và tên *")
        phone = st.text_input("Số điện thoại *")
        email = st.text_input("Email")
        card_type = st.selectbox(
            "Loại thẻ",
            ["Thẻ ghi nợ nội địa", "Thẻ ghi nợ quốc tế",
             "Thẻ tín dụng"]
        )
        card_method = st.radio(
            "Phương thức nhận thẻ",
            ["Nhận tại quầy", "Đăng ký nhận tại nhà"]
        )

        agree = st.checkbox(
            "Tôi xác nhận thông tin cung cấp là chính xác."
        )

        submitted = st.form_submit_button(
            "GỬI YÊU CẦU MỞ THẺ",
            use_container_width=True
        )

        if submitted:
            if not name.strip() or not phone.strip():
                st.error("Vui lòng nhập họ tên và số điện thoại.")
            elif not phone.strip().isdigit() or len(phone.strip()) not in range(9, 12):
                st.error("Số điện thoại chưa hợp lệ.")
            elif not agree:
                st.warning("Vui lòng xác nhận thông tin.")
            else:
                code = save_request(
                    "Mở thẻ ngân hàng",
                    name.strip(),
                    f"Loại thẻ: {card_type}; Nhận thẻ: {card_method}"
                )
                st.session_state.cards.append({
                    "Mã yêu cầu": code,
                    "Họ và tên": name.strip(),
                    "Loại thẻ": card_type
                })
                st.success(f"Đã ghi nhận yêu cầu! Mã yêu cầu: {code}")


# =========================
# 2. MỞ TÀI KHOẢN
# =========================
elif menu == "👤 Mở tài khoản":

    st.subheader("👤 ĐĂNG KÝ MỞ TÀI KHOẢN")
    st.write("Đăng ký thông tin cơ bản để yêu cầu mở tài khoản.")

    with st.form("account_form"):

        name = st.text_input("Họ và tên *")
        phone = st.text_input("Số điện thoại *")
        email = st.text_input("Địa chỉ email")
        birth = st.date_input(
            "Ngày sinh",
            value=datetime(2000, 1, 1),
            min_value=datetime(1920, 1, 1),
            max_value=datetime.today()
        )
        account_type = st.selectbox(
            "Loại tài khoản",
            ["Tài khoản thanh toán cá nhân",
             "Tài khoản nhận lương",
             "Tài khoản trực tuyến"]
        )

        agree = st.checkbox(
            "Tôi đồng ý gửi thông tin đăng ký."
        )

        submitted = st.form_submit_button(
            "ĐĂNG KÝ TÀI KHOẢN",
            use_container_width=True
        )

        if submitted:
            if not name.strip() or not phone.strip():
                st.error("Vui lòng nhập họ tên và số điện thoại.")
            elif not phone.strip().isdigit() or len(phone.strip()) not in range(9, 12):
                st.error("Số điện thoại chưa hợp lệ.")
            elif not agree:
                st.warning("Vui lòng xác nhận trước khi đăng ký.")
            else:
                code = save_request(
                    "Mở tài khoản",
                    name.strip(),
                    f"Loại tài khoản: {account_type}; "
                    f"Ngày sinh: {birth}; Email: {email}"
                )
                st.success(
                    f"Đăng ký thành công! Mã yêu cầu: {code}"
                )
# =========================
# 3. GỬI TIẾT KIỆM
# =========================
elif menu == "💰 Gửi tiết kiệm":

    st.subheader("💰 GỬI TIẾT KIỆM")
    st.write(
        "Nhập số tiền, kỳ hạn và lãi suất giả định "
        "để tính số tiền lãi dự kiến."
    )

    with st.form("savings_form"):

        name = st.text_input("Họ và tên *")
        phone = st.text_input("Số điện thoại *")

        amount = st.number_input(
            "Số tiền gửi (VNĐ)",
            min_value=1000000,
            value=10000000,
            step=1000000
        )

        months = st.selectbox(
            "Kỳ hạn gửi",
            [1, 3, 6, 9, 12, 18, 24],
            format_func=lambda x: f"{x} tháng"
        )

        rate = st.number_input(
            "Lãi suất năm giả định (%)",
            min_value=0.0,
            max_value=20.0,
            value=4.5,
            step=0.1
        )

        submitted = st.form_submit_button(
            "TÍNH LÃI VÀ ĐĂNG KÝ",
            use_container_width=True
        )

        if submitted:
            if not name.strip() or not phone.strip():
                st.error("Vui lòng nhập họ tên và số điện thoại.")
            elif not phone.strip().isdigit() or len(phone.strip()) not in range(9, 12):
                st.error("Số điện thoại chưa hợp lệ.")
            else:
                interest = amount * (rate / 100) * months / 12
                total = amount + interest

                code = save_request(
                    "Gửi tiết kiệm",
                    name.strip(),
                    f"Số tiền: {amount:,.0f} VNĐ; "
                    f"Kỳ hạn: {months} tháng; Lãi suất giả định: {rate}%"
                )

                st.session_state.savings.append({
                    "Mã yêu cầu": code,
                    "Họ và tên": name.strip(),
                    "Số tiền gửi": amount,
                    "Kỳ hạn (tháng)": months,
                    "Lãi dự kiến": interest
                })

                st.success(f"Đã ghi nhận yêu cầu! Mã: {code}")

                col1, col2, col3 = st.columns(3)
                col1.metric("Tiền gửi", f"{amount:,.0f} đ")
                col2.metric("Tiền lãi dự kiến", f"{interest:,.0f} đ")
                col3.metric("Tổng tiền dự kiến", f"{total:,.0f} đ")

                st.caption(
                    "Lưu ý: Đây là phép tính lãi đơn minh họa, "
                    "chưa tính thuế, phí hoặc cách tính lãi thực tế. "
                    "Lãi suất trên không phải lãi suất chào bán của ngân hàng."
                )


# =========================
# 4. VAY VỐN NGÂN HÀNG
# =========================
elif menu == "🏦 Vay vốn ngân hàng":

    st.subheader("🏦 ĐĂNG KÝ NHU CẦU VAY VỐN")
    st.write("Gửi nhu cầu vay để được tư vấn về hồ sơ và điều kiện.")

    with st.form("loan_form"):

        name = st.text_input("Họ và tên *")
        phone = st.text_input("Số điện thoại *")

        loan_type = st.selectbox(
            "Mục đích vay",
            ["Vay tiêu dùng", "Vay mua nhà",
             "Vay mua xe", "Vay kinh doanh", "Mục đích khác"]
        )

        amount = st.number_input(
            "Số tiền muốn vay (VNĐ)",
            min_value=1000000,
            value=50000000,
            step=5000000
        )

        months = st.selectbox(
            "Thời hạn vay dự kiến",
            [6, 12, 24, 36, 60, 120, 240],
            format_func=lambda x: f"{x} tháng"
        )

        income = st.selectbox(
            "Nguồn thu nhập",
            ["Lương hàng tháng", "Kinh doanh",
             "Lao động tự do", "Nguồn thu nhập khác"]
        )

        submitted = st.form_submit_button(
            "GỬI YÊU CẦU VAY VỐN",
            use_container_width=True
        )

        if submitted:
            if not name.strip() or not phone.strip():
                st.error("Vui lòng nhập họ tên và số điện thoại.")
            elif not phone.strip().isdigit() or len(phone.strip()) not in range(9, 12):
                st.error("Số điện thoại chưa hợp lệ.")
            else:
                code = save_request(
                    "Vay vốn ngân hàng",
                    name.strip(),
                    f"Mục đích: {loan_type}; "
                    f"Số tiền: {amount:,.0f} VNĐ; "
                    f"Kỳ hạn: {months} tháng; Thu nhập: {income}"
                )

                st.session_state.loans.append({
                    "Mã yêu cầu": code,
                    "Họ và tên": name.strip(),
                    "Mục đích vay": loan_type,
                    "Số tiền vay": amount,
                    "Thời hạn (tháng)": months
                })

                st.success(
                    f"Đã tiếp nhận yêu cầu tư vấn. Mã: {code}"
                )
                st.info(
                    "Yêu cầu này chưa phải hợp đồng vay và "
                    "không đồng nghĩa với việc khoản vay được duyệt."
                )


# =========================
# QUẢN LÝ ĐĂNG KÝ
# =========================
elif menu == "📋 Quản lý đăng ký":

    st.subheader("📋 DANH SÁCH YÊU CẦU ĐĂNG KÝ")

    requests = get_all_requests()

    if not requests:
        st.info("Chưa có yêu cầu đăng ký nào.")
    else:
        df = pd.DataFrame(requests)

        service_filter = st.selectbox(
            "Lọc theo dịch vụ",
            ["Tất cả"] + df["Dịch vụ"].unique().tolist()
        )

        if service_filter != "Tất cả":
            df = df[df["Dịch vụ"] == service_filter]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "📥 TẢI DANH SÁCH CSV",
            data=csv,
            file_name="thienbank_dang_ky.csv",
            mime="text/csv"
        )
    "© 2026 DemoBank | Ứng dụng mô phỏng ngân hàng số phục vụ học tập."
