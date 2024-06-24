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

    cursor.execute('SELECT appointmentID, ownerID , vetID, AppointmentDate, appStatus from Appointment')
    appDetails = []
    for row in cursor.fetchall():
       appDetails.append(row)

    cursor.execute('SELECT vetID, charges from VetAvailability')
    vetCostDetails = []
    for row in cursor.fetchall():
       vetCostDetails.append(row)
    
    cursor.execute('SELECT appointmentID, testID from LabTestBooked')
    labBookedDetails = []
    for row in cursor.fetchall():
       labBookedDetails.append(row)
    
    cursor.execute('SELECT testID, testCost from LabTests')
    labTestDetails = []
    for row in cursor.fetchall():
       labTestDetails.append(row)
    

    for element in appDetails:
        if (element[4]=='Completed'):
            appointment_id = element [0]
            owner_id = element [1]
            vet_id = element [2]
            appDate =datetime.strptime(element [3], '%Y-%m-%d')
            
            for element in vetCostDetails:
                if (vet_id == element [0]):
                    vet_cost = element [1]
                    break

            for element in labBookedDetails:
                if(appointment_id == element[0]):
                    test_id = element[1]
                    for element in labTestDetails:
                        if(test_id == element[0]):
                            test_cost = element[1]
                            break
            
            
            payDate = fake.date_between(start_date=appDate, end_date='+10d')
            payDate = datetime.strftime(payDate, '%Y-%m-%d')
            

            # SQL query to insert data into the Appointment table
            sql_insert_query = """
            INSERT INTO Payment (appointmentID, ownerID, vetID, vetCharges, testID, labTestCharges, paymentDate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(sql_insert_query, (appointment_id, owner_id, vet_id, vet_cost, test_id, test_cost, payDate))
            conn.commit()
                
    # Close connections
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")