import json
import os

def update_json_file(filename, key, update_func):
    """
    Generic function to update a JSON file.
    
    Args:
        filename (str): Path to the JSON file
        key (str): The key to update in the JSON data
        update_func (callable): A function that takes the data for the key and updates it
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the current data
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
            
        # Check if the key exists
        if key in data:
            # Update the data using the provided function
            update_func(data[key])
        else:
            print(f"Error: '{key}' not found in the file {filename}")
            return False
            
        # Write the updated data back to the file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
        return True
    except Exception as e:
        print(f"Error updating JSON file: {e}")
        return False