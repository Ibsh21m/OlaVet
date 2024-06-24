import pyodbc
from faker import Faker
import random
from datetime import datetime

pet_names = [
    "Abigail", "Ace", "Adam", "Addie", "Admiral", "Aggie", "Aires", "Aj", "Ajax", "Aldo", "Alex", "Alexus", "Alf",
    "Alfie", "Allie", "Ally", "Amber", "Amie", "Amigo", "Amos", "Amy", "Andy", "Angel", "Angus", "Annie", "Apollo",
    "April", "Archie", "Argus", "Aries", "Armanti", "Arnie", "Arrow", "Ashes", "Ashley", "Astro", "Athena", "Atlas",
    "Audi", "Augie", "Aussie", "Austin", "Autumn", "Axel", "Axle", "Babbles","Babykins", "Bacchus", "Bailey", "Bam-bam", 
    "Bambi", "Bandit", "Banjo", "Barbie", "Barclay", "Barker", "Barkley", "Barley", "Barnaby", "Barney", "Baron", "Bart", 
    "Basil", "Baxter", "Beamer", "Beanie", "Beans", "Bear", "Beau", "Beauty", "Beaux", "Bebe", "Beetle", "Bella", "Belle",
    "Ben", "Benji", "Benny", "Benson", "Bentley", "Bernie", "Bessie", "Biablo", "Bibbles", "Big Boy", "Biggie", "Billie",
    "Billy", "Bingo", "Binky", "Birdie", "Biscuit", "Bishop", "Gus", "Guy", "Gypsy", "Hailey", "Haley", "Hallie", "Hamlet",
    "Hank", "Hanna", "Hannah", "Hans", "Happy", "Hardy", "Harley", "Harpo", "Harrison", "Harry", "Harvey", "Heather",
    "Heidi", "Henry", "Hercules", "Hershey", "Higgins", "Hobbes", "Holly", "Homer", "Honey", "Honey-Bear", "Hooch",
    "Hoover", "Hope", "Houdini", "Howie", "Hudson", "Huey", "Hugh", "Hugo", "Humphrey", "Hunter", "India", "Indy",
    "Iris", "Isabella", "Isabelle", "Itsy", "Itsy-bitsy", "Ivory", "Ivy", "Izzy", "Jack", "Jackie", "Jackpot",
    "Jackson", "Jade", "Jagger", "Jags", "Jaguar", "Jake", "Jamie", "Jasmine", "Jasper", "Jaxson", "Jazmie", "Jazz",
    "Jelly", "Jelly-bean", "Jenna", "Jenny", "Jerry", "Jersey", "Jess", "Jesse", "Jesse James", "Jessie", "Jester",
    "Jet", "Jethro", "Jett", "Jetta", "Jewel", "Jewels", "Jimmy", "Jingles", "JJ", "Joe", "Joey", "Johnny", "Jojo",
    "Joker", "Jolie", "Jolly", "Jordan", "Josie", "Joy", "JR", "Judy", "Julius", "June", "Misty", "Mitch", "Mittens",
    "Mitzi", "Mitzy", "Mo", "Mocha", "Mollie", "Molly", "Mona", "Muffy", "Nakita", "Nala", "Nana", "Natasha", "Nellie",
    "Nemo", "Nena", "Peanut", "Peanuts", "Pearl", "Pebbles", "Penny", "Phoebe", "Phoenix", "Sara", "Sarah", "Sasha",
    "Sassie", "Sassy", "Savannah", "Scarlett", "Shasta", "Sheba", "Sheena", "Shelby", "Shelly", "Sienna", "Sierra",
    "Silky", "Silver", "Simone", "Sissy", "Skeeter", "Sky", "Skye", "Skyler", "Waldo", "Wallace", "Wally", "Walter",
    "Wayne", "Weaver", "Webster", "Wesley", "Westie"
]
breeds = { "Dog" : ["Labrador","German Shepherd", "Rottweiler", "Poodle"], "Bird":["Macaw","Budgie", "Cockatiel", "Duck"], "Cat": ["Persian", "Sphynx", "Siamese"], "Horse" :["Arabian", "Mustang", "Gypsy Horse"], "Snake": ["Python", "Red-Tailed Boas","Rosy Boas"], "Cattle":["Wagyu", "Ayrshire", "Brahman"], "Chicken": ["Leghorn", "Orpington"], "Goat":["Nubian","Beetal"], "Sheep": ["Hampshire", "Suffolk"]}

pet_types = ["Bird", "Dog", "Cat", "Horse", "Snake", "Cattle", "Chicken", "Goat", "Sheep"]

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

    cursor.execute("SELECT ownerID FROM Owner")
    owner_ids = []
    for row in cursor.fetchall():
         owner_ids.append(row)

    # Generate and insert fake pet records for each owner
    for element in owner_ids:
        owner_id = element[0]
        # Determine the number of pets each owner will have (at least one)
        num_pets = random.randint(1, 3)  # Generate a random number of pets for each owner (between 1 and 3)

        for _ in range(num_pets):
            pet_name = random.choice(pet_names)
            pet_type = random.choice(pet_types)
            if pet_type == "Dog":
                 breed = random.choice(breeds["Dog"])
                 date_of_birth = fake.date_of_birth(minimum_age=4, maximum_age=10)  # Generate date of birth between 4 and 10 years ago
                 pet_weight = round(random.uniform(20, 70), 2)  # Generate a random weight between 1 and 70
            elif pet_type == "Bird":
                 breed = random.choice(breeds["Bird"])
                 date_of_birth = fake.date_of_birth(minimum_age=1, maximum_age=3)  # Generate date of birth between 1 and 3 years ago
                 pet_weight = round(random.uniform(0.5, 4), 2)  # Generate a random weight between 0.5 and 4
            elif pet_type == "Cat":
                 breed = random.choice(breeds["Cat"])
                 date_of_birth = fake.date_of_birth(minimum_age=3, maximum_age=14)  # Generate date of birth between 3 and 14 years ago
                 pet_weight = round(random.uniform(3.6, 8), 2)  # Generate a random weight between 3.6 and 8
            elif pet_type == "Horse":
                 breed = random.choice(breeds["Horse"])
                 date_of_birth = fake.date_of_birth(minimum_age=5, maximum_age=20)  # Generate date of birth between 5 and 20 years ago
                 pet_weight = round(random.uniform(300, 800), 2)  # Generate a random weight between 300 and 800
            elif pet_type == "Snake":
                 breed = random.choice(breeds["Snake"])
                 date_of_birth = fake.date_of_birth(minimum_age=2, maximum_age=9)  # Generate date of birth between 2 and 9 years ago
                 pet_weight = round(random.uniform(0.6, 15), 2)  # Generate a random weight between 0.6 and 15
            elif pet_type == "Cattle":
                 breed = random.choice(breeds["Cattle"])
                 date_of_birth = fake.date_of_birth(minimum_age=2, maximum_age=10)  # Generate date of birth between 2 and 10 years ago
                 pet_weight = round(random.uniform(200, 750), 2)  # Generate a random weight between 200 and 750
            elif pet_type == "Chicken":
                 breed = random.choice(breeds["Chicken"])
                 date_of_birth = fake.date_of_birth(minimum_age=2, maximum_age=6)  # Generate date of birth between 2 and 6 years ago
                 pet_weight = round(random.uniform(1.5, 3.5), 2)  # Generate a random weight between 1.5 and 3.5
            elif pet_type == "Sheep":
                 breed = random.choice(breeds["Sheep"])
                 date_of_birth = fake.date_of_birth(minimum_age=3, maximum_age=10)  # Generate date of birth between 3 and 10 years ago
                 pet_weight = round(random.uniform(30, 80), 2)  # Generate a random weight between 200 and 750
            else:
                 breed = random.choice(breeds["Goat"])
                 date_of_birth = fake.date_of_birth(minimum_age=3, maximum_age=10)  # Generate date of birth between 3 and 10 years ago
                 pet_weight = round(random.uniform(30, 80), 2)  # Generate a random weight between 200 and 750

            gender = fake.random_element(elements=('Male', 'Female'))
            is_vaccinated = fake.boolean()

            # SQL query to insert fake data into the Pet table for each owner
            sql_insert_query = f"""
            INSERT INTO Pet (petName, ownerID, type, breed, DateOfBirth, petWeight, gender, isVaccinated)
            VALUES ('{pet_name}', {owner_id}, '{pet_type}', '{breed}', '{date_of_birth}', {pet_weight}, '{gender}', {int(is_vaccinated)})
            """
            cursor.execute(sql_insert_query)
            conn.commit()


    # Close connections
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")