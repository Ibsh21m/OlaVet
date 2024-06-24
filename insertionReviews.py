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


    good_reviews = ["Great experience, very knowledgeable doctor!","The doctor was friendly and helpful.","Highly recommend this doctor, very professional.","Excellent service and care from the doctor."]

    bad_reviews = ["Average experience, didn't fully address my concerns.","Didn't feel satisfied with the consultation.","The doctor seemed inattentive and rushed.","Not happy with the treatment provided.","The doctor lacked empathy and understanding.","Overall, a disappointing experience with the doctor."]

    cursor.execute('SELECT appointmentID, vetID, AppointmentDate, appStatus from Appointment')
    appDetails = []
    for row in cursor.fetchall():
       appDetails.append(row)

  
    for element in appDetails:
        if (element[3]=='Completed'):
            appointment_id = element [0]
            vet_id = element [1]
            appDate = element[2]
            review_date = fake.date(appDate)
            rating = random.randint(2,5)
            if rating <= 3:
                review_text = fake.random_element(bad_reviews)
            else:
                review_text = fake.random_element(good_reviews)

            # SQL query to insert data into the Appointment table
            sql_insert_query = """
            INSERT INTO Review (vetID, appointmentID, rating, reviewText, reviewDate)
            VALUES (?, ?, ?, ?, ?)
            """
            
            cursor.execute(sql_insert_query, vet_id, appointment_id, rating, review_text, review_date)
            conn.commit()
                

    # Close connections
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")