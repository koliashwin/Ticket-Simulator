from datetime import datetime
import json
import os
import random
import qrcode

from DataManager import DataManager

class TicketGenerator:
    """Class to handle ticket generation related operations."""
    
    def __init__(self, qr_codes_folder='qr_codes'):
        self.qr_codes_folder = qr_codes_folder
        self.db_manager = DataManager()

    def generate_ticket(self, data):
        """
        Generate a ticket with a unique ID, timestamp, source, destination, and ticket cost.
        Save the ticket data in a QR code.
        """
        # Generate a unique/random ticket ID
        ticket_id = self.generate_ticket_id()
        qr_code_filename = f'{ticket_id}.png'     # unique name for ticket
        timestamp = str(datetime.now())         # Track ticket timings

        ticket_cost = self.ticket_cost(data['from'], data['to'])

        insert_query = '''
        INSERT INTO Tickets (ticket_id, timestamp, from_station, to_station, ticket_cost, QR_Code, status)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        '''
        ticket_data = (ticket_id, timestamp, data['from'], data['to'], ticket_cost, qr_code_filename, 'N')
        
        self.db_manager.execute_query(insert_query, ticket_data)

        self.generate_qr_code(ticket_id, qr_code_filename)    # function to generate qr code

        return ticket_data, qr_code_filename
    
    def generate_card(self, data):
        card_id = random.randint(1000,9999)
        card_type = data['type']

        if card_type == 'trip':
            cols = 'trips, from_station, to_station'
            vals = '%s, %s, %s'
            card_data = (card_id, data['user'], data['contact'], data['type'], data['trips'], data['from'], data['to'])
        else:                   # for card_type = balacne
            cols = 'balance'
            vals = '%s'
            card_data = (card_id, data['user'], data['contact'], data['type'], data['balance'])
        insert_query = f'''
        INSERT INTO CARDS (card_id, user_name, user_contact, type, {cols})
        VALUES(%s, %s, %s, %s, {vals})
        '''
        print("insert query : ", insert_query)
        self.db_manager.execute_query(insert_query, card_data)
        return card_data

    
    def ticket_cost(self, soruce_station, destination_station):
        """
        Calculate ticket cost based on the following logic:
        cost = (abs(source_station - destination_station) - 1) * 10
        Minimum cost is 10.
        """
        cost = (abs(soruce_station - destination_station)-1)*10
        return cost if cost>=10 else 10
    
    def generate_ticket_id(self):
        # uinque/random id generator
        return f'TKT-{random.randint(1000,9999)}'
    
    def generate_qr_code(self, data, filename, folder='qr_codes'):
        """Generate a QR code with the provided data and save it to a file."""
        # create folder if not exsist
        os.makedirs(folder, exist_ok=True)

        # construct fullpath for qr code file
        filepath = os.path.join(folder,filename)
        json_data_str = json.dumps(data)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(json_data_str)
        qr.make(fit=True)

        img = qr.make_image(fill_color='black', back_color='white')
        img.save(filepath)
        print("qr_code_file path : ", filepath)
        img.close()