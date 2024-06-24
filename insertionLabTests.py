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

    cursor.execute("SELECT LabID FROM Labs")
    LabIDs = [row[0] for row in cursor.fetchall()]

    test_info = [("Fecal Testing", random.randint(20,40)), ("Urinalysis", random.randint(15,25)), ("    Complete BLood Count (CBC)", random.randint(30,40)), ("Ultrasound", random.randint(45,60)), ("X-Ray", random.randint(50, 80)), ("Endoscopy", random.randint(100,140)), ("Biopsy", random.randint(80,100)), ("MRI", random.randint(120,190)), ("Heartworm Test", random.randint(20,40)), ("Bacterial Culture",random.randint(120,150)), ("Anti-microbial Sensitivity", random.randint(180,200)), ("Cogulation Time", random.randint(90,100))]

    for lab_id in LabIDs:
        for i in range(random.randint(5,12)):
            test_name , test_cost = test_info [i]
            sql_insert_query = f"""
            INSERT INTO LabTests (labID, testName, testCost)
            VALUES ('{lab_id}', '{test_name}', '{test_cost}')
            """
            cursor.execute(sql_insert_query)
            conn.commit()

    # Close connections
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")