from datetime import datetime

import mysql.connector

try:
    import database_reservation as db
except ImportError:
    try:
        import database_reservation as db
    except ImportError:
        import database_reservation


def ask_required(prompt, max_length):
    while True:
        value = input(prompt).strip()
        if not value:
            print("Kailangan itong punan.")
        elif len(value) > max_length:
            print(f"Hindi dapat lumampas sa {max_length} characters.")
        else:
            return value


def ask_positive_int(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and int(value) >= 1:
            return int(value)
        print("Dapat numero ito na higit sa 0.")


def is_valid_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def ask_date(prompt):
    while True:
        value = input(prompt).strip()
        if not is_valid_date_format(value):
            print("Gamitin ang format na YYYY-MM-DD (halimbawa: 2026-10-27).")
            continue
        return value


def ask_time(prompt):
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%H:%M")
            return value
        except ValueError:
            print("Gamitin ang format na HH:MM (24-hour).")


def display_record(record):
    print(
        f"\nReservation No.:   {record['reservation_no']}\n"
        f"Requester Name:    {record['requester_name']}\n"
        f"Department:        {record['department']}\n"
        f"Room Name:         {record['room_name']}\n"
        f"Participants:      {record['participants']}\n"
        f"Reservation Date:  {record['reservation_date']}\n"
        f"Start Time:        {record['start_time']}\n"
        f"End Time:          {record['end_time']}\n"
        f"Purpose:           {record['purpose']}\n"
        f"Status:            {record['status']}\n"
        f"Encoded By:        {record['encoded_by']}\n"
        f"Created At:        {record['created_at']}"
    )


def reserve_room():
    print("\n--- Mag-record ng bagong Room Reservation ---")
    reservation_no = db.get_next_reservation_no()
    print(f"Reservation No.: {reservation_no}")

    requester_name = ask_required("Buong pangalan ng requester: ", 150)
    department = ask_required("Departamento/Office: ", 100)
    room_name = ask_required("Pangalan ng silid: ", 100)
    participants = ask_positive_int("Bilang ng kalahok: ")
    reservation_date = ask_date("Petsa ng reservation (YYYY-MM-DD): ")
    start_time = ask_time("Oras ng pagsisimula (HH:MM): ")
    end_time = ask_time("Oras ng pagtatapos (HH:MM): ")

    try:
        s = datetime.strptime(start_time, "%H:%M")
        e = datetime.strptime(end_time, "%H:%M")
        if e <= s:
            print("Hindi valid ang end time. Dapat mas huli ang end time kaysa sa start time.")
            return
    except ValueError:
        print("Hindi wastong oras.")
        return

    purpose = ask_required("Layunin ng paggamit: ", 255)
    encoded_by = ask_required("In-record ni: ", 100)

    record = {
        "reservation_no": reservation_no,
        "requester_name": requester_name,
        "department": department,
        "room_name": room_name,
        "participants": participants,
        "reservation_date": reservation_date,
        "start_time": start_time,
        "end_time": end_time,
        "purpose": purpose,
        "status": "Confirmed",
        "encoded_by": encoded_by,
    }

    try:
        record_id = db.insert_reservation(record)
        print(f"Matagumpay na na-reserve ang silid! ID: {record_id}")
    except mysql.connector.IntegrityError:
        print("May record na gamit ang reservation number na ito.")
    except mysql.connector.Error as error:
        print(f"Hindi na-save ang record: {error}")


def show_all_reservations():
    try:
        records = db.get_all_reservations()
    except mysql.connector.Error as error:
        print(f"Hindi makuha ang mga reservation records: {error}")
        return

    print("\n--- Lahat ng Room Reservations ---")
    if not records:
        print("Wala pang room reservations.")
        return

    for record in records:
        display_record(record)


def search_reservation():
    reservation_no = ask_required("Reservation No. na hahanapin: ", 20)
    try:
        record = db.get_reservation_by_no(reservation_no)
    except mysql.connector.Error as error:
        print(f"Hindi mahanap ang record: {error}")
        return

    if record is None:
        print("Walang record na may reservation number na iyan.")
        return

    display_record(record)


def cancel_room_reservation():
    reservation_no = ask_required("Reservation No. na ise-cancel: ", 20)
    try:
        record = db.get_reservation_by_no(reservation_no)
    except mysql.connector.Error as error:
        print(f"Hindi makuha ang record: {error}")
        return

    if record is None:
        print("Walang record na may reservation number na iyan.")
        return

    if record["status"] == "Cancelled":
        print("Ang reservation na ito ay nakansela na.")
        return

    display_record(record)
    confirmation = input("Sigurado ka bang ise-cancel ang reservation na ito? (o/h): ").strip().lower()
    if confirmation not in {"o", "oo", "y", "yes"}:
        print("Kinansela ang cancellation.")
        return

    try:
        updated = db.cancel_reservation(reservation_no)
    except mysql.connector.Error as error:
        print(f"Hindi ma-update ang record: {error}")
        return

    if updated:
        print("Matagumpay na nakansela ang reservation!")
    else:
        print("Hindi na-update ang record.")


def remove_reservation():
    reservation_no = ask_required("Reservation No. na buburahin: ", 20)
    try:
        record = db.get_reservation_by_no(reservation_no)
    except mysql.connector.Error as error:
        print(f"Hindi makuha ang record: {error}")
        return

    if record is None:
        print("Walang record na may reservation number na iyan.")
        return

    display_record(record)
    confirmation = input("Sigurado ka bang buburahin ang record na ito? (o/h): ").strip().lower()
    if confirmation not in {"o", "oo", "y", "yes"}:
        print("Kinansela ang pagbura.")
        return

    try:
        deleted = db.delete_reservation(reservation_no)
    except mysql.connector.Error as error:
        print(f"Hindi nabura ang record: {error}")
        return

    if deleted:
        print("Matagumpay na nabura ang reservation record.")
    else:
        print("Wala nang record na buburahin.")


def remove_all_reservations():
    confirmation = input(
        "Sigurado ka bang buburahin ang LAHAT ng room reservations? (o/h): "
    ).strip().lower()
    if confirmation not in {"o", "oo", "y", "yes"}:
        print("Kinansela ang pagbura ng lahat ng records.")
        return

    try:
        deleted_count = db.delete_all_reservations()
    except mysql.connector.Error as error:
        print(f"Hindi nabura ang lahat ng records: {error}")
        return

    if deleted_count:
        print(f"Matagumpay na nabura ang {deleted_count} reservation records.")
    else:
        print("Walang room reservations na buburahin.")
