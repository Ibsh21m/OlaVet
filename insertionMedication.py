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

    medicine_list = [
    "Methimazole",
    "Prednisolone",
    "Pimobendan",
    "Fluoxetine",
    "Metronidazole",
    "Budesonide",
    "Chlorambucil",
    "Ursodiol",
    "Amlodipine",
    "Doxycycline",
    "Reconcile",
    "Vetmedin",
    "Clomicalm",
    "Apoquel",
    "Clavamox",
    "Cerenia",
    "Prednistab",
    "Trazodone",
    "Carprovet",
    "Simparica Trio"
]

    cursor.execute('SELECT appointmentID, petID, vetID, AppointmentDate, appStatus from Appointment')
    appDetails = []
    for row in cursor.fetchall():
       appDetails.append(row)

    cursor.execute('SELECT vetID, vetName from Vet')
    vetDetails = []
    for row in cursor.fetchall():
        vetDetails.append(row)

  
    for element in appDetails:
        if (element[4]=='Completed'):
            appointment_id = element [0]
            pet_id = element [1]
            vet_id = element [2]
            appDate = element[3]
            datePre = fake.date(appDate)
            for element in vetDetails:
                if (vet_id == element [0]):
                    vet_name = element [1]
                    break
            med_name = random.choice(medicine_list)
            dosage = fake.random_element(["Once","Twice","Thrice","During Discomfort"])
            duration = fake.random_element([3, 7, 10, 15, 20])

            # SQL query to insert data into the Appointment table
            sql_insert_query = f"""
            INSERT INTO Medication (appointmentID, vetID, prescribedBy, petID, medicationName, dosage_per_day, duration_in_days, date_prescribed)
            VALUES ({appointment_id}, {vet_id}, '{vet_name}', {pet_id}, '{med_name}', '{dosage}', {duration}, '{datePre}')
            """
            cursor.execute(sql_insert_query)
            conn.commit()
                

    # Close connections
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")