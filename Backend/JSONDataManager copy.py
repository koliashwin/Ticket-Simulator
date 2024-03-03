import json
import logging
import os
from textwrap import indent

class DataManager:
    Data_File = r'D:\Git-hub repo\Metro QR\MyData.json'

    @classmethod
    def load_data(cls):
        """
        Load data from the specified JSON file.

        Returns:
            dict: Loaded data if successful, otherwise None.
        """
        try:
            with open(cls.Data_File, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            logging.error(f'Error: {cls.Data_File} not found')
            return None
    
    @classmethod
    def add_data(cls, data, table_obj):
        existing_data = cls.load_data()
        existing_data.setdefault(table_obj,[])
        existing_data[table_obj].append(data)

        cls.save_data(existing_data)
        
    @classmethod
    def save_data(cls, data):
        with open(cls.Data_File, 'w') as file:
            json.dump(data, file, indent=4)
    
    @classmethod
    def update_item(cls, table_obj, item_id, update_field, new_val):
        print("inside update_item...")
        try:
            data = cls.load_data()
            items = data.get(table_obj, [])
            # print(items)
            for item in items:
                if item.get('id') == item_id:
                    item[update_field] = new_val
            if cls.save_data(item):
                return True, item
            else:
                logging.error("Failed to save updated data")
                return False, None
            # logging.warning(f"Item with id {item_id} not found in {table_obj}")
            # return False, None
        except FileNotFoundError:
            logging.error(f'Error : {cls.Data_File} not found')
            return False, None
    
    def display_data_list(obj_list, description):
        """
        Display a list of objects with indices and prompt the user to choose an item.

        Args:
            obj_list (list): List of objects to display.
            description (str): Description of the objects being displayed.

        Returns:
            dict or None: Chosen object if successful, otherwise None.
        """
        for idx, item in enumerate(obj_list, 1):
            print(f"{idx}. {item['name']}")
        choice = int(input(f"choose {description}: "))
        return obj_list[choice-1] if 1<=choice<=len(obj_list) else None