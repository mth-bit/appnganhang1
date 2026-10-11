import streamlit as st
from datetime import datetime
import uuid

st.set_page_config(
    page_title="Banking Demo",
    page_icon="🏦",
    layout="centered"
)

# ===== DEMO CONFIGURATION =====
DEMO_USER = "sinhvien"
DEMO_PASS = "123456"

# ===== SESSION DATA =====
defaults = {
    "logged_in": False,
    "balance": 5_000_000,
    "history": [],
    "account_requests": [],
    "card_requests": [],
    "savings": [],
    "loans": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ===== STYLE =====
st.markdown("""
<style>
.stApp { background-color: #f3f7f4; }
.block-container { max-width: 850px; padding-top: 2rem; }
h1, h2, h3 { color: #087443; }
div.stButton > button {
    background-color: #087443;
    color: white;
    border-radius: 8px;
    min-height: 42px;
}
.demo-banner {
    background: #fff3cd;
    color: #664d03;
    padding: 12px;
    border-radius: 8px;
    text-align: center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="demo-banner">
BẢN MÔ PHỎNG HỌC TẬP — KHÔNG PHẢI ỨNG DỤNG NGÂN HÀNG CHÍNH THỨC
</div>
""", unsafe_allow_html=True)

def log_action(service, detail, amount=0):
    st.session_state.history.insert(0, {
        "Mã demo": uuid.uuid4().hex[:8].upper(),
        "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Dịch vụ": service,
        "Nội dung": detail,
        "Số tiền minh họa (VNĐ)": int(amount),
        "Trạng thái": "HOÀN TẤT (DEMO)"
    })

# ===== LOGIN =====
if not st.session_state.logged_in:
    st.title("🏦 BANKING DEMO")
    st.subheader("Đăng nhập")

    st.info("Tài khoản demo: sinhvien | Mật khẩu: 123456")

    with st.form("login"):
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        submit = st.form_submit_button("Đăng nhập")

    if submit:
        if username == DEMO_USER and password == DEMO_PASS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Thông tin đăng nhập demo không đúng.")

    st.stop()

# ===== SIDEBAR =====
st.sidebar.title("BANKING DEMO")
st.sidebar.caption("Ngân hàng số mô phỏng")

page = st.sidebar.radio(
    "CHỌN DỊCH VỤ",
    [
        "Trang chủ",
        "1. Mở tài khoản",
        "2. Mở thẻ",
        "3. Gửi tiết kiệm",
        "4. Vay vốn",
        "5. Chuyển tiền",
        "6. Lịch sử giao dịch"
    ]
)

if st.sidebar.button("Đăng xuất"):
    st.session_state.logged_in = False
    st.rerun()

# ===== HOME =====
if page == "Trang chủ":
    st.title("Xin chào, Sinh viên!")
    st.write("Chào mừng đến với hệ thống ngân hàng mô phỏng.")

    st.metric("Số dư demo", f"{st.session_state.balance:,.0f} VNĐ")

    st.subheader("Các dịch vụ")
    st.markdown("""
    - 📝 Mở tài khoản trực tuyến
    - 💳 Đăng ký thẻ mô phỏng
    - 💰 Gửi tiết kiệm và tính lãi
    - 🏠 Mô phỏng khoản vay
    - 💸 Chuyển tiền giả lập
    - 📋 Theo dõi lịch sử thao tác
    """)

    st.info("Chọn dịch vụ ở thanh menu bên trái để bắt đầu.")

# ===== 1. OPEN ACCOUNT =====
elif page == "1. Mở tài khoản":
    st.title("📝 Mở tài khoản demo")
    st.write("Điền thông tin mẫu để minh họa quy trình đăng ký.")

    with st.form("account_form"):
        name = st.text_input("Họ và tên minh họa")
        email = st.text_input("Email mẫu")
        phone = st.text_input("Số điện thoại mẫu")
        account_type = st.selectbox(
            "Loại tài khoản",
            ["Tài khoản thanh toán demo", "Tài khoản số đẹp demo"]
        )
        submit = st.form_submit_button("Gửi đăng ký")

    if submit:
        if not name.strip() or not email.strip() or not phone.strip():
            st.error("Vui lòng điền đầy đủ các trường.")
        else:
            request = {
                "Mã hồ sơ demo": uuid.uuid4().hex[:8].upper(),
                "Họ tên": name,
                "Email mẫu": email,
                "Điện thoại mẫu": phone,
                "Loại tài khoản": account_type,
                "Trạng thái": "Đã tiếp nhận mô phỏng"
            }
            st.session_state.account_requests.append(request)
            log_action("Mở tài khoản", account_type)
            st.success("Đăng ký mô phỏng hoàn tất!")
            st.json(request)

    if st.session_state.account_requests:
        st.subheader("Hồ sơ demo đã tạo")
        st.dataframe(
            st.session_state.account_requests,
            use_container_width=True
        )

# ===== 2. OPEN CARD =====
elif page == "2. Mở thẻ":
    st.title("💳 Đăng ký thẻ demo")
    st.write("Chọn loại thẻ để xem minh họa.")

    with st.form("card_form"):
        owner = st.text_input("Tên chủ thẻ minh họa")
        card_type = st.selectbox(
            "Loại thẻ",
            ["Thẻ ghi nợ demo", "Thẻ tín dụng demo"]
        )
        card_style = st.selectbox(
            "Phong cách thẻ",
            ["Xanh lá", "Đen", "Xanh dương"]
        )
        submit = st.form_submit_button("Đăng ký thẻ demo")

    if submit:
        if not owner.strip():
            st.error("Vui lòng nhập tên minh họa.")
        else:
            card = {
                "Mã hồ sơ demo": uuid.uuid4().hex[:8].upper(),
                "Chủ thẻ": owner,
                "Loại thẻ": card_type,
                "Phong cách": card_style,
                "Số thẻ": "DEMO **
** 1234",
                "Trạng thái": "Đăng ký mô phỏng hoàn tất"
            }
            st.session_state.card_requests.append(card)
            log_action("Mở thẻ", card_type)
            st.success("Đăng ký thẻ demo thành công!")

            st.markdown(f"""
            <div style="background:#087443;color:white;
                        padding:25px;border-radius:16px">
                <h3 style="color:white">BANKING DEMO</h3>
                <p>THẺ MÔ PHỎNG — KHÔNG CÓ GIÁ TRỊ THANH TOÁN</p>
                <h2 style="color:white">DEMO **
** 1234</h2>
                <p>CHỦ THẺ: {owner}</p>
                <p>{card_type}</p>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.card_requests:
        st.subheader("Hồ sơ thẻ demo")
        st.dataframe(
            st.session_state.card_requests,
            use_container_width=True
        )

# ===== 3. SAVINGS =====
elif page == "3. Gửi tiết kiệm":
    st.title("💰 Gửi tiết kiệm demo")
    st.caption("Lãi suất bên dưới là giả định phục vụ bài thuyết trình.")

    with st.form("savings_form"):
        principal = st.number_input(
            "Số tiền gửi (VNĐ)",
            min_value=100_000,
            value=1_000_000,
            step=100_000
        )
        months = st.selectbox("Kỳ hạn", [1, 3, 6, 9, 12, 24])
        rate = st.number_input(
            "Lãi suất năm giả định (%)",
            min_value=0.0,
            max_value=20.0,
            value=4.5,
            step=0.1
        )
        submit = st.form_submit_button("Tính tiền lãi")

    if submit:
        interest = int(principal * (rate / 100) * months / 12)
        total = int(principal) + interest

        st.success("Đã tính kết quả minh họa!")
        st.metric("Tiền gửi", f"{principal:,.0f} VNĐ")
        st.metric("Lãi dự kiến", f"{interest:,.0f} VNĐ")
        st.metric("Tổng cuối kỳ", f"{total:,.0f} VNĐ")

        st.caption(
            "Công thức đơn giản: Tiền gửi × lãi suất năm × số tháng / 12. "
            "Không phải báo giá hay cam kết lãi suất thực."
        )

        if st.button("Lưu hồ sơ tiết kiệm demo"):
            record = {
                "Mã demo": uuid.uuid4().hex[:8].upper(),
                "Tiền gửi": int(principal),
                "Kỳ hạn (tháng)": months,
                "Lãi suất giả định (%)": rate,
                "Lãi minh họa": interest,
                "Tổng cuối kỳ minh họa": total
            }
            st.session_state.savings.append(record)
            log_action("Gửi tiết kiệm", f"Kỳ hạn {months} tháng", principal)
            st.success("Đã lưu hồ sơ mô phỏng.")

    if st.session_state.savings:
        st.subheader("Hồ sơ tiết kiệm demo")
        st.dataframe(st.session_state.savings, use_container_width=True)

# ===== 4. LOAN =====
elif page == "4. Vay vốn":
    st.title("🏠 Tính khoản vay demo")
    st.caption("Lãi suất giả định; kết quả chỉ phục vụ minh họa.")

    with st.form("loan_form"):
        principal = st.number_input(
            "Số tiền vay (VNĐ)",
            min_value=1_000_000,
            value=20_000_000,
            step=1_000_000
        )
        months = st.selectbox(
            "Thời hạn vay (tháng)",
            [6, 12, 24, 36, 48, 60]
        )
        rate = st.number_input(
            "Lãi suất năm giả định (%)",
            min_value=0.0,
            max_value=30.0,
            value=8.0,
            step=0.5
        )
        submit = st.form_submit_button("Tính khoản trả")

    if submit:
        monthly_rate = rate / 100 / 12

        if monthly_rate == 0:
            payment = principal / months
        else:
            payment = (
                principal * monthly_rate
                / (1 - (1 + monthly_rate) ** (-months))
            )

        total = payment * months
        interest = total - principal

        st.success("Đã tính khoản vay minh họa!")
        st.metric("Khoản vay", f"{principal:,.0f} VNĐ")
        st.metric("Trả mỗi tháng ước tính", f"{payment:,.0f} VNĐ")
        st.metric("Tổng lãi ước tính", f"{interest:,.0f} VNĐ")
        st.metric("Tổng trả ước tính", f"{total:,.0f} VNĐ")

        if st.button("Lưu hồ sơ vay demo"):
            record = {
                "Mã demo": uuid.uuid4().hex[:8].upper(),
                "Số tiền vay": int(principal),
                "Thời hạn (tháng)": months,
                "Lãi suất giả định (%)": rate,
                "Khoản trả tháng minh họa": round(payment),
                "Tổng trả minh họa": round(total)
            }
            st.session_state.loans.append(record)
            log_action("Vay vốn", f"Thời hạn {months} tháng", principal)
            st.success("Đã lưu hồ sơ vay mô phỏng.")

    if st.session_state.loans:
        st.subheader("Hồ sơ vay demo")
        st.dataframe(st.session_state.loans, use_container_width=True)

# ===== 5. TRANSFER =====
elif page == "5. Chuyển tiền":
    st.title("💸 Chuyển tiền demo")
    st.metric("Số dư demo", f"{st.session_state.balance:,.0f} VNĐ")

    with st.form("transfer_form"):
        recipient = st.text_input("Tên người nhận")
        account = st.text_input("Số tài khoản minh họa")
        bank = st.selectbox(
            "Ngân hàng minh họa",
            ["Ngân hàng Demo A", "Ngân hàng Demo B", "Ngân hàng Demo C"]
        )
        amount = st.number_input(
            "Số tiền chuyển (VNĐ)",
            min_value=0,
            value=100_000,
            step=50_000
        )
        message = st.text_input("Nội dung chuyển tiền")
        submit = st.form_submit_button("Xác nhận chuyển tiền")

    if submit:
        if not recipient.strip() or not account.strip():
            st.error("Vui lòng nhập người nhận và tài khoản minh họa.")
        elif amount <= 0:
            st.error("Số tiền phải lớn hơn 0.")
        elif amount > st.session_state.balance:
            st.error("Số dư demo không đủ.")
        else:
            st.session_state.balance -= int(amount)
            tx_id = uuid.uuid4().hex[:8].upper()
            log_action(
                "Chuyển tiền",
                f"Người nhận: {recipient}; TK demo: {account}; "
                f"{bank}; Nội dung: {message}; Mã: {tx_id}",
                amount
            )
            st.success("✅ GIAO DỊCH MÔ PHỎNG THÀNH CÔNG!")
            st.write(f"*Mã giao dịch demo:* {tx_id}")
            st.write(f"*Người nhận:* {recipient}")
            st.write(f"*Ngân hàng minh họa:* {bank}")
            st.write(f"*Số tiền:* {amount:,.0f} VNĐ")
            st.write(f"*Số dư demo còn lại:* {st.session_state.balance:,.0f} VNĐ")

# ===== 6. HISTORY =====
elif page == "6. Lịch sử giao dịch":
    st.title("📋 Lịch sử thao tác demo")

    if st.session_state.history:
        st.dataframe(
            st.session_state.history,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Chưa có thao tác nào. Hãy thử một dịch vụ demo.")

    st.subheader("Tổng hợp hồ sơ demo")
    st.write("Hồ sơ mở tài khoản:", len(st.session_state.account_requests))
    st.write("Hồ sơ mở thẻ:", len(st.session_state.card_requests))
    st.write("Hồ sơ tiết kiệm:", len(st.session_state.savings))
    st.write("Hồ sơ vay vốn:", len(st.session_state.loans))

st.divider()
st.caption(
    "BANKING DEMO — Dự án học tập. Không thuộc Vietcombank. "
    "Không kết nối tài khoản thật, không phát hành thẻ, "
    "không tiếp nhận hồ sơ tài chính thật và không chuyển tiền thật."
)
