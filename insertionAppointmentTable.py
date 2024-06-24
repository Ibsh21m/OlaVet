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

    # Fetching owner, vet, and pet data
    cursor.execute("SELECT ownerID, regDate FROM Owner")
    owners = []
    for row in cursor.fetchall():
       owners.append(row)
    

    cursor.execute("SELECT vetID, specialization, regDate FROM Vet")
    vets = []
    for row in cursor.fetchall():
        vets.append(row)  # Append each row to the list
   

    cursor.execute("SELECT petID, ownerID, type FROM Pet")
    pets = []
    for row in cursor.fetchall():
       pets.append(row)  # Append each row to the list
    
    cursor.execute("SELECT vetID, startTime FROM VetAvailability")
    vet_avail = []
    for row in cursor.fetchall():
       vet_avail.append(row)
    #print(vet_avail)

    # Inserting appointments
    for _ in range(10000):  # Inserting 10 appointments as an example
        pet_id, ownerID, pet_type = fake.random_element(pets)
        vet_id, vet_specialization, vet_regDate = fake.random_element(vets)

        for element in owners:
            if(ownerID == element[0]):
                owner_regDate = element[1]
                print(owner_regDate)
                print(vet_regDate)
                start_date = max(owner_regDate, vet_regDate)
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime('2023-11-01', '%Y-%m-%d')
                break

        for element in vet_avail:
            if (vet_id == element[0]):
                givenTime = element[1]
                timePart = givenTime.split('.')

                obtainedTime = datetime.strptime(timePart[0], '%H:%M:%S')
                gap = random.choice([10,15,20,25,30,40,50,60])
                appTime = obtainedTime + timedelta(minutes=gap)
                start_time = appTime.strftime('%H:%M:%S')
                break

        # Check if the pet type and vet specialization are allowed together
        if vet_specialization in pet_vet_mapping.get(pet_type, []):
            appointment_date = fake.date_between_dates(date_start = start_date , date_end = end_date)
            status = fake.random_element(['Scheduled', 'Canceled', 'Completed'])
            reason = fake.random_element(['Check Up','Lab Reports','Vaccination','Disease Diagnosis'])

            # SQL query to insert data into the Appointment table
            sql_insert_query = f"""
            INSERT INTO Appointment (ownerID, vetID, petID, AppointmentDate, StartTime, appStatus, reasonForVisit, VetSpecialization, PetType)
            VALUES ({ownerID}, {vet_id}, {pet_id}, '{appointment_date}', '{start_time}', '{status}', '{reason}', '{vet_specialization}', '{pet_type}')
            """
            cursor.execute(sql_insert_query)
            conn.commit()
        
    # Close connections
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")