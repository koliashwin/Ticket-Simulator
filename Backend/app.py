import logging
from QrCodeScanner import QrCodeScanner
from TicketGenerator import TicketGenerator
from DataManager import DataManager
from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app)

sample_data = [
    {'id': 1, 'name':'item 1'},
    {'id': 2, 'name':'item 2'},
    {'id': 3, 'name':'item 3'}
]
ticket_generator = TicketGenerator()
@app.route('/api/stations', methods=['GET'])
def get_all_stations():
    try:
        data_manager = DataManager()
        qry = 'select * from stations'
        station_list = data_manager.get_tbl_item_list(table_name='stations', cols=['id','name'])
        # print(jsonify(station_list))
        return jsonify(station_list)
    except Exception as e:
        logging.error(f'Error getting all stations : {e}')
        return jsonify({'error': 'filed to fetch stations'})

@app.route('/api/generate', methods=['POST'])
def generate_ticket():
    try:
        stations = request.get_json()
        source_id = int(stations['source'])
        destination_id = int(stations['destination'])
        
        ticket_cost = ticket_generator.ticket_cost(source_id, destination_id)

        json_data = {
            'from': source_id,
            'to': destination_id,
            'cost': ticket_cost
        }

        ticket_data = ticket_generator.generate_ticket(json_data)
        return jsonify("ticket Data : ", ticket_data)
    except Exception as e:
        logging.error(f'Error while generating ticket : {e}')
        return jsonify({'error': 'filed to generate ticket'})
    
@app.route('/api/scan/<int:scanner>', methods=['GET'])
def scan_ticket(scanner):
    try:
        print(f'scan_type : {scanner}')
        qr_code_scanner = QrCodeScanner()
        
        scanned_data = qr_code_scanner.scan_realtime_qr_code(check_in=scanner)
        print(f'ticket data : {scanned_data}')
        return jsonify('scanner opened')
    except Exception as e:
        logging.error(f'Error while scaning ticket : {e}')
        return jsonify({'error': 'filed to scan ticket'})

@app.route('/api/generate_pass', methods=['POST'])
def generate_pass():
    try:
        payload= request.get_json()
        print('data recieved : ',payload)
        user_name = payload['user_name']
        user_contact = payload['user_contact']

        if (payload['pass_type']=='trip'):
            source_id = int(payload['source_station'])
            destination_id = int(payload['destination'])
            trips = int(payload['trips'])
            pass_info = {
                'type': 'trip',
                'trips':trips,
                'from':source_id,
                'to':destination_id,
                'user':user_name,
                'contact':user_contact
            }
        elif (payload['pass_type']=='balance'):
            balance = int(payload['balance'])
            pass_info = {
                'type': 'balance',
                'balance': balance,
                'user':user_name,
                'contact':user_contact
            }
        pass_data = ticket_generator.generate_card(pass_info)
        logging.info('Pass gernerated success fully ')
        return jsonify('Pass Created successfully')
    except Exception as e:
        logging.error(f'Error while generating Pass : {e}')
        return jsonify({'error': 'filed to generate pass'})

# -----------------------
@app.route('/api/data', methods=['GET'])
def get_data():
    # data = sample_data
    return jsonify(sample_data)

@app.route('/api/data/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in sample_data if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({'error': 'Item not found'}), 404
    
@app.route('/api/data', methods=['POST'])
def add_item():
    data = request.get_json()

    if 'name' in data:
        new_item = {'id': len(sample_data)+1, 'name':data['name']}
        sample_data.append(new_item)
        return jsonify(new_item), 201
    else:
        return jsonify({'error': 'Missing data: name'}), 400

@app.route('/api/data/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = next((item for item in sample_data if item['id'] == item_id), None)
    
    if item:
        if 'name' in data:
            item['name'] = data['name']
            return jsonify(item)
        else:
            return jsonify({'error' : 'Missing data: name'}), 400
    else:
        return jsonify({'error' : 'Item not found'}), 404

@app.route('/api/data/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global sample_data
    sample_data = [item for item in sample_data if item['id'] != item_id]
    return jsonify({'message': 'item deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)