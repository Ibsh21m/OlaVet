import pyodbc
from faker import Faker
import random
from datetime import datetime, timedelta

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

    pet_vet_mapping = {
    'Dog': ['Canine', 'Surgery', 'Zoological Medicine', 'Dentistry', 'Nutritionist'],
    'Bird': ['Avian', 'Surgery', 'Zoological Medicine', 'Dentistry', 'Nutritionist'],
    'Cat': ['Feline', 'Surgery', 'Zoological Medicine', 'Dentistry', 'Nutritionist'],
    'Horse': ['Equine', 'Surgery', 'Zoological Medicine', 'Dentistry', 'Nutritionist'],
    'Snake': ['Reptile', 'Surgery', 'Zoological Medicine', 'Dentistry', 'Nutritionist'],
    'Cattle': ['Cattle', 'Dairy', 'Surgery', 'Zoological Medicine', 'Dentistry', 'Nutritionist'],
    'Chicken': ['Poultry', 'Avian', 'Surgery', 'Zoological Medicine', 'Dentistry', 'Nutritionist'],
    'Goat': ['Cattle', 'Dairy', 'Surgery', 'Zoological Medicine', 'Dentistry', 'Nutritionist'],
    'Sheep': ['Cattle', 'Dairy', 'Surgery', 'Zoological Medicine', 'Dentistry', 'Nutritionist']}

    
    cursor.execute('SELECT appointmentID, petID, AppointmentDate, appStatus from Appointment')
    appDetails = []
    for row in cursor.fetchall():
       appDetails.append(row)

    cursor.execute('SELECT labID, testID, testName from LabTests')
    labTestDetails = []
    for row in cursor.fetchall():
        labTestDetails.append(row)

  
    for element in appDetails:
        lab_id, test_id, test_name = fake.random_element(labTestDetails)
        if (element[3]=='Completed'):
            appointment_id = element [0]
            pet_id = element [1]
            appDate = element[2]
            start_date = datetime.strptime(appDate, '%Y-%m-%d')
            end_date = datetime.strptime('2023-11-01', '%Y-%m-%d')
            test_date = fake.date_between_dates(date_start = start_date , date_end = end_date)
            test_result = fake.random_element(["Pending","Waiting Sample","Dispatched"])
            # SQL query to insert data into the Appointment table
            sql_insert_query = f"""
            INSERT INTO LabTestBooked (appointmentID, petID, testID, testName, labID, testDate, testResult)
            VALUES ({appointment_id}, {pet_id}, {test_id}, '{test_name}', {lab_id}, '{test_date}', '{test_result}')
            """
            cursor.execute(sql_insert_query)
            conn.commit()
                

    # Close connections
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")