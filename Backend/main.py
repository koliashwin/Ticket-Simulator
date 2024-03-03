import logging
from DataManager import DataManager
from QrCodeScanner import QrCodeScanner
from TicketGenerator import TicketGenerator

logging.basicConfig(level=logging.INFO)

if __name__=='__main__':
    data_manager = DataManager()
    ticket_generator = TicketGenerator()
    qr_code_scanner = QrCodeScanner()

    try:
        data_manager.create_tables()
        while True:
            print("1. Generate Ticket\n2. Check-In scanner\n3. Check-Out scanner\n4. Exit")
            try:
                choice = int(input("Enter a number: "))

                if choice == 1:
                    stations = data_manager.get_tbl_item_list('Stations',['name'])
                    source_station = data_manager.select_station(stations, 'Source')
                    destination_station = data_manager.select_station(stations, 'Destination')
                    ticket_cost = ticket_generator.ticket_cost(source_station['id'], destination_station['id'])
                    if source_station and destination_station and source_station != destination_station:
                        logging.info("Source Station: %s, Destination Station: %s",source_station, destination_station)
                        json_data = {
                            'from' : source_station['id'],
                            'to': destination_station['id'],
                            'cost': ticket_cost
                        }
                        ticket_data, qr_code_filename = ticket_generator.generate_ticket(json_data)
                        logging.info("Ticket generated successfully.")
                        logging.info("Ticket Data: %s", ticket_data)
                        logging.info("QR Code Filename: %s", qr_code_filename)
                    else:
                        logging.error("Invalid station selection")

                elif choice == 2:
                    logging.info("Scanning for QR Codes in real_time. press 'q' to exit")
                    scanned_data = qr_code_scanner.scan_realtime_qr_code()

                    if scanned_data:
                        # print("try print :",scanned_data)
                        logging.info("Scanned data: %s", scanned_data)
                        # qr_code_scanner.display_qr_result(scanned_data)
                        logging.info("Welcome! Enjoy your journey.")
                
                elif choice == 3:
                    logging.info("Scanning for QR Codes in real_time. press 'q' to exit")
                    scanned_data = qr_code_scanner.scan_realtime_qr_code(check_in=False)

                    if scanned_data:
                        # print("try print :",scanned_data)
                        logging.info("Scanned data: %s", scanned_data)
                        # qr_code_scanner.display_qr_result(scanned_data)
                        logging.info("Take Care! See you soon again.")
                        
                elif choice == 4:
                    logging.info("Exiting the program. Goodbye!")
                    break

                else:
                    logging.error("Invalid choice. Please re-enter.")
            except ValueError:
                logging.error("Invalid input. please enter a number")
    finally:
        data_manager.disconnect()