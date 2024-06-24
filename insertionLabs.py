import pyodbc
from faker import Faker
import random

cities = { "Cheshire" : ["Chester","Macclesfield", "Alsager", "Congleton"], "Kent":["Ashford","Maidstone", "Dover", "Canterbury"], "Sussex": ["Brighton", "Rye", "Arundel"]}
counties = ["Cheshire", "Kent", "Sussex"]

# Set up connection parameters
server = 'eNIGMA\\SQLEXPRESS'  # Replace 'your_server_name' with your server name
database = 'OlaVet_1'  # Replace 'your_database_name' with your database name
username = 'sa'  # Replace 'your_username' with your username
password = 'ibshaam21'  # Replace 'your_password' with your password
driver = '{SQL Server}'  # Driver for SQL Server

# Create connection string
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # Establish connection
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    fake = Faker()

    labNames = ["Batt Labs", "Nation Wide Labs", "LPD Labs", "PALS Vet Labs"]
    locations = {"Batt Labs" : [9904, 9907, 9908, 9901], "Nation Wide Labs":[9902, 9905, 9907, 9909], "LPD Labs":[9903, 9904, 9900], "PALS Vet Labs":[9909, 9906, 9900]}

    for lab_name in labNames:
        location_ids = locations.get(lab_name, [])  # Get the location IDs for the current lab name
        for loc_id in location_ids:
            # Inserting data into the Labs table
            sql_insert_query = f"""
            INSERT INTO Labs (labName, locationID)
            VALUES ('{lab_name}', '{loc_id}')
            """
            cursor.execute(sql_insert_query)
            conn.commit()

    # Close connections
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")