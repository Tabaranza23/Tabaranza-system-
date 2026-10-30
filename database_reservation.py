import os

import mysql.connector
from mysql.connector import Error


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "room_reservation")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
    )


def test_connection():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM room_reservations LIMIT 1")
            cursor.fetchone()
            return True, f"Nakakonekta sa MySQL database '{DB_NAME}'."
        return False, "Hindi makakonekta sa MySQL."
    except Error as error:
        return False, str(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_next_reservation_no():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT reservation_no FROM room_reservations ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if not result:
            return "RS-001"
        last_no = result[0]
        try:
            num = int(last_no.split("-")[1]) + 1
            return f"RS-{num:03d}"
        except (IndexError, ValueError):
            return "RS-001"
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_all_reservations():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, reservation_no, requester_name, department, room_name,
                   participants, reservation_date, start_time, end_time,
                   purpose, status, encoded_by, created_at
            FROM room_reservations
            ORDER BY id DESC
            """
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_reservation_by_no(reservation_no):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, reservation_no, requester_name, department, room_name,
                   participants, reservation_date, start_time, end_time,
                   purpose, status, encoded_by, created_at
            FROM room_reservations
            WHERE reservation_no = %s
            """,
            (reservation_no,),
        )
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def insert_reservation(record):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO room_reservations
                (reservation_no, requester_name, department, room_name,
                 participants, reservation_date, start_time, end_time,
                 purpose, status, encoded_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                record["reservation_no"],
                record["requester_name"],
                record["department"],
                record["room_name"],
                record["participants"],
                record["reservation_date"],
                record["start_time"],
                record["end_time"],
                record["purpose"],
                record["status"],
                record["encoded_by"],
            ),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def cancel_reservation(reservation_no):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE room_reservations
            SET status = %s
            WHERE reservation_no = %s AND status = %s
            """,
            ("Cancelled", reservation_no, "Confirmed"),
        )
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_reservation(reservation_no):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM room_reservations WHERE reservation_no = %s", (reservation_no,))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_all_reservations():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM room_reservations")
        connection.commit()
        return cursor.rowcount
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
