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

    # Generate and insert fake records into the Location table
    for i in range(25): # Inserting 10 fake records as an example
        county = random.choice(counties)
        if county == "Cheshire":
            city = random.choice(cities["Cheshire"])
        elif county == "Kent":
            city = random.choice(cities["Kent"])
        else:
            city = random.choice(cities["Sussex"])
        zip_code = fake.zipcode()

        # SQL query to insert fake data into the Location table
        # Check if the record with the same county and city already exists
        sql_check_query = f"SELECT COUNT(*) FROM Location WHERE city = '{city}' AND county = '{county}'"
        cursor.execute(sql_check_query)
        count = cursor.fetchone()[0]

        if count == 0:  # Insert only if the record does not exist
            cursor.execute("INSERT INTO Location (city, county, zipCode) VALUES (?, ?, ?)", city, county, zip_code)
        
        conn.commit()

    # Close connections
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")