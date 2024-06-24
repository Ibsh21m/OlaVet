import pyodbc
from faker import Faker
import random
from datetime import datetime

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

    cursor.execute("SELECT city, county, zipCode FROM Location")
    locations = cursor.fetchall()

    # Set your desired starting and ending dates for registration
    start_date = '2022-01-01'  # Replace with your starting date
    end_date = '2023-11-01'    # Replace with your ending date
    # Set your desired starting and ending dates for registration
    start_date = datetime.strptime('2022-01-01', '%Y-%m-%d')  # Replace with your starting date
    end_date = datetime.strptime('2023-11-01', '%Y-%m-%d')    # Replace with your ending date


    # Generate and insert fake records into the Vet table
    for i in range(700):  # Insert 10 fake records as an example
        vet_name = "Dr " + gen_name_without_prefix()
        specialization = random.choice(vet_spec)

        # Choose a random domain from the email_domains list
        domain = random.choice(email_domains)
        # Create a custom email using the vet's name and chosen domain
        email = vet_name.lower().replace(" ", ".") + domain
        
        phone = gen_phone()

        # Choose random location data from the fetched Location data
        city, county, zip_code = random.choice(locations)

        is_certified = 1  # Randomly set IsCertified to 0 or 1
        reg_date = fake.date_between_dates(date_start=start_date, date_end=end_date)
        # SQL query to insert fake data into the Vet table
        sql_insert_query = f"""INSERT INTO Vet (vetName, specialization, Email, Phone, city, county, zipCode, IsCertified, regDate) VALUES ('{vet_name}', '{specialization}', '{email}', '{phone}', '{city}', '{county}', '{zip_code}', {is_certified},'{reg_date}')"""
        cursor.execute(sql_insert_query)
        conn.commit()

    # Close connections
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")