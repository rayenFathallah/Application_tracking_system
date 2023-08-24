import json

# Create a list of dictionaries
def export_data_json(data,file_name) : 
# Convert the list of dictionaries to a JSON string
    json_string = json.dumps(data)

    # Open a file in write mode
    with open('data/clean_data/'+file_name, 'w') as f:

        # Write the JSON string to the file
        f.write(json_string)

    # Close the file
    f.close()