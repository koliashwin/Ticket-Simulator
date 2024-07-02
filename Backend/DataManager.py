from turtle import update
from uu import Error
import mysql.connector
import logging

class DataManager:
    def __init__(self, host='localhost', user='root', password='root', database='metro_qr'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            logging.info("Connected to MySQL database")
        except mysql.connector.Error as err:
            logging.error(f"Error connecting MySQL DB : {err}")
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            logging.info("Disconnected from MySQL DB")
    
    def create_tables(self):
        try:
            self.connect()
            query = '''
            CREATE TABLE IF NOT EXISTS Stations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
            '''
            self.execute_query(query)

            query = '''
            CREATE TABLE IF NOT EXISTS Tickets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ticket_id VARCHAR(50) NOT NULL,
                timestamp DATETIME,
                from_station INT,
                to_station INT,
                ticket_cost INT,
                QR_Code VARCHAR(255),
                status VARCHAR(1),
                FOREIGN KEY (from_station) REFERENCES Stations(id),
                FOREIGN KEY (to_station) REFERENCES Stations(id)
            )
            '''
            self.execute_query(query)

            query = '''
            CREATE TABLE IF NOT EXISTS CARDS (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            user_contact VARCHAR(10) UNIQUE,
            card_id INT UNIQUE,
            type VARCHAR(50) NOT NULL,
            created_on DATE DEFAULT (CURRENT_DATE),
            validity DATE,
            trips INT,
            balance FLOAT,
            from_station INT,
            to_station INT,
            FOREIGN KEY (from_station) REFERENCES Stations(id),
            FOREIGN KEY (to_station) REFERENCES Stations(id)
            )
            '''
            self.execute_query(query)
        finally:
            self.disconnect()
    
    def execute_query(self, query, data=None):
        db_cursor = None
        try:
            if not self.connection:
                self.connect()
            db_cursor = self.connection.cursor()
            if data:
                db_cursor.execute(query, data)
            else:
                db_cursor.execute(query)
            self.connection.commit()
            logging.info("Query executed successfully")
        except mysql.connector.Error as err:
            logging.error(f"Error executing query: {err}")
        # finally:
        #     if db_cursor:
        #         db_cursor.close()
        #     self.disconnect()
    
    def get_tbl_item_list(self, table_name, cols=None):
        try:
            self.connect()
            if cols:
                query = f"SELECT {', '.join(item for item in cols)} FROM {table_name}"
            else:
                query = f"SELECT * FROM {table_name}"
            print("get_tbl_item qry : ", query)
            db_cursor = self.connection.cursor(dictionary=True)
            db_cursor.execute(query)
            stations = db_cursor.fetchall()
            return stations
        except mysql.connector.Error as err:
            logging.error(f"Error retrieving stations: {err}")
            return[]
        # finally:
        #     if db_cursor:
        #         db_cursor.close()
        #     self.disconnect()
    
    
    def select_station(self, stations, type):
        try:
            print("Available Stations :")
            for station in stations:
                print(f"{station['id']}. {station['name']}")
            station_id = int(input(f"{type} station: "))
            selected_station = next((station for station in stations if station['id']==station_id), None)
            if selected_station:
                return selected_station
            else:
                logging.error("Invalid station selected")
                return None
        except ValueError:
            logging.error("Invalid input. enter valid number")
            return None
        
    def update_ticket_status(self, ticket_id, scan_type):
        try:
            self.connect()
            query = "SELECT id, status FROM Tickets WHERE ticket_id = %s"
            db_cursor = self.connection.cursor(dictionary=True)
            db_cursor.execute(query, (ticket_id,))
            ticket = db_cursor.fetchone()
            if ticket:
                if ticket['status'] == 'N' and scan_type=="check_in":
                    update_query = "UPDATE Tickets SET status = 'S' WHERE ticket_id = %s"
                    self.execute_query(update_query, (ticket_id,))
                    logging.info("Welcome! your journey has started.")

                elif ticket['status'] == 'S' and scan_type=="check_out":
                    update_query = "UPDATE Tickets SET status = 'F' WHERE ticket_id = %s"
                    self.execute_query(update_query, (ticket_id,))
                    logging.info("Tack Care... Be sure to visit again")
                else:
                    logging.error(f"Invalid Ticket status: {ticket['status']}")
            else:
                logging.error(f"Ticket not found in database")
        except mysql.connector.Error as err:
            logging.error(f"Error updating ticket status: {err}")
        # finally:
        #     self.disconnect()