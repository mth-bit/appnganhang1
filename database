import pandas as pd
from database import save_request, get_all_requests
import sqlite3
from datetime import datetime

DB_NAME = "Demobank.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_code TEXT UNIQUE NOT NULL,
            service TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            details TEXT,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Chờ xử lý'
        )
    """)

    conn.commit()
    conn.close()


def save_request(service, customer, details):
    conn = get_connection()

    created_at = datetime.now().strftime("%d/%m/%Y %H:%M")

    cursor = conn.execute("""
        INSERT INTO requests (
            request_code,
            service,
            customer_name,
            details,
            created_at,
            status
        )
        VALUES (
            lower(hex(randomblob(6))),
            ?, ?, ?, ?, 'Chờ xử lý'
        )
    """, (service, customer, details, created_at))

    conn.commit()

    row = conn.execute(
        "SELECT request_code FROM requests WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    request_code = row["request_code"].upper()

    conn.execute(
        "UPDATE requests SET request_code = ? WHERE id = ?",
        (request_code, cursor.lastrowid)
    )

    conn.commit()
    conn.close()

    return request_code


def get_all_requests():
    conn = get_connection()

    rows = conn.execute("""
        SELECT
            request_code AS 'Mã yêu cầu',
            service AS 'Dịch vụ',
            customer_name AS 'Họ và tên',
            details AS 'Thông tin',
            created_at AS 'Ngày đăng ký',
            status AS 'Trạng thái'
        FROM requests
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# Tạo bảng dữ liệu khi khởi tạo ứng dụng
create_database()
