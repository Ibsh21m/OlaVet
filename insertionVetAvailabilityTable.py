import pyodbc
from faker import Faker
import random
from datetime import datetime, timedelta

vet_spec = ["Avian", "Feline", "Canine", "Equine", "Cattle", "Dairy", "Poultry", "Reptiles", "Surgey", "Dentistry", "Nutritionist", "Zological Medicine"]
email_domains = ["@gmail.com", "@icloud.com", "@hotmail.com", "@yahoo.com"]

def gen_phone():
     # Generate random numbers for each part of the phone number
    country_code = "44"  # Assuming +44 for UK country code
    area_code = fake.random_int(min=100, max=999)
    local_number = fake.random_number(digits=6)  # Generates a 6-digit local number

    # Format the phone number as +44-123-4567890
    formatted_number = f"+{country_code}-{area_code}-{local_number}"
    return formatted_number

def gen_name_without_prefix():
    name = fake.name()
    # Remove common prefixes if present
    prefixes = ["Mrs ", "Mr ", "Ms ", "Dr ","Miss "]
    for prefix in prefixes:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break  # Remove only the first matching prefix

    return name

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

    fake = Faker(['en_GB'])

    # Fetch VetIDs from Vets table
    cursor.execute("SELECT vetID FROM Vet")
    vet_ids = []
    for row in cursor.fetchall():
       vet_ids.append(row)


    # Insert availability for each vet
    for element in vet_ids:
        vet_id = element[0]
        availabilities_count = random.choice([1, 2])  # Randomly choose 1 or 2 availabilities per vet
        # Generate random start and end times
        start_time_1 = fake.time(pattern="%H:%M")
        end_time_1= fake.time(pattern="%H:%M")
        # Ensure start time is before end time
        while start_time_1 >= end_time_1:
            start_time_1 = fake.time(pattern="%H:%M")
            end_time_1 = fake.time(pattern="%H:%M")

        charges = round(random.uniform(50, 200), 2)  # Random charges between 50 and 200

        # SQL query to insert data into the VetAvailability table for the first availability
        sql_insert_query = """
        INSERT INTO VetAvailability (vetID, startTime, endTime, charges)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql_insert_query, (vet_id, start_time_1, end_time_1, charges))
        conn.commit()

        if availabilities_count == 2:
            # Generate random start and end times
            start_time_2 = fake.time(pattern="%H:%M")
            end_time_2= fake.time(pattern="%H:%M")
            # Ensure start time is before end time
            while  start_time_2 <= end_time_1:
                start_time_2 = fake.time(pattern="%H:%M")
            while start_time_2 >= end_time_2:
                end_time_2 = fake.time(pattern="%H:%M")
            
            charges = round(random.uniform(50, 200), 2)  # Random charges between 50 and 200

            # SQL query to insert data into the VetAvailability table for the second availability
            sql_insert_query = """
            INSERT INTO VetAvailability (vetID, startTime, endTime, charges)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(sql_insert_query, (vet_id, start_time_2, end_time_2, charges))
            conn.commit()
        

    # Close connections
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")