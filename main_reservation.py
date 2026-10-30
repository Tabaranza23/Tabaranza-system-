try:
    import database_reservation as db
except ImportError:
    import reservations


import reservations


def main():
    connected, message = db.test_connection()
    if not connected:
        print(f"Hindi makakonekta sa XAMPP MySQL: {message}")
        print("Siguruhin na naka-start ang MySQL at na-import ang schema_room_reservation.sql.")
        return
    print(message)

    print("\n=== ROOM RESERVATION SYSTEM ===")
    while True:
        print("\n[1] Mag-record ng bagong Room Reservation")
        print("[2] Tingnan ang Lahat ng Reservations")
        print("[3] Hanapin ang Reservation (by Reservation No.)")
        print("[4] Cancel ang Reservation")
        print("[5] Burahin ang Reservation Record")
        print("[6] Burahin ang Lahat ng Reservation Records")
        print("[0] Lumabas")
        choice = input("Piliin: ").strip()

        if choice == "1":
            reservations.reserve_room()
        elif choice == "2":
            reservations.show_all_reservations()
        elif choice == "3":
            reservations.search_reservation()
        elif choice == "4":
            reservations.cancel_room_reservation()
        elif choice == "5":
            reservations.remove_reservation()
        elif choice == "6":
            reservations.remove_all_reservations()
        elif choice == "0":
            print("Salamat! Paalam.")
            break
        else:
            print("Hindi wastong pagpili. Pumili ng 1, 2, 3, 4, 5, 6, o 0.")


if __name__ == "__main__":
    main()
