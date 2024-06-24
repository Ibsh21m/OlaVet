create database OlaVet_1;
Select @@SERVERNAME

use OlaVet_1;

--DROP TABLES
drop table Payment
drop table Owner
drop table Pet
drop table Vet
drop table Location
drop table VetAvailability
drop table Appointment
drop table Labs
drop table LabTests
drop table LabTestBooked
drop table Review
drop table Medication

CREATE TABLE Owner (
    ownerID INT IDENTITY(1,1) PRIMARY KEY,
    fullName VARCHAR(100),
	email VARCHAR(100),
    phone VARCHAR(20),
    city VARCHAR(50),
    county VARCHAR(50),
    zipCode VARCHAR(20),
    regDate DATE,
	CONSTRAINT FK_Owner_Location FOREIGN KEY (city, county, zipCode) REFERENCES Location (city, county, zipCode)
);

CREATE TABLE Pet (
    petID INT IDENTITY(1,1) PRIMARY KEY,
    petName VARCHAR(50),
    ownerID INT FOREIGN KEY REFERENCES Owner(ownerID),
    type VARCHAR(50),
	breed VARCHAR(50),
    DateOfBirth DATE,
	age AS CONVERT(INT, DATEDIFF(YEAR, DateOfBirth, GETDATE())),
    petWeight DECIMAL(5, 2),
    gender VARCHAR(10),
    isVaccinated BIT,
);

CREATE TABLE Vet (
    vetID INT IDENTITY(1000,1) PRIMARY KEY,
    vetName VARCHAR(100),
    specialization VARCHAR(100),
	Email VARCHAR(100),
    Phone VARCHAR(20),
    city VARCHAR(50),
    county VARCHAR(50),
    zipCode VARCHAR(20),
    IsCertified BIT,
	regDate DATE,
	CONSTRAINT FK_Vet_Location FOREIGN KEY (city, county, zipCode) REFERENCES Location (city, county, zipCode)
);
ALTER TABLE Vet
ADD CONSTRAINT UQ_vetName UNIQUE(vetID, vetName);

CREATE TABLE Location (
    locationID INT IDENTITY(9900,1) PRIMARY KEY,
    city VARCHAR(50),
    county VARCHAR(50),
    zipCode VARCHAR(20),
	CONSTRAINT UC_City_State_Zip_Country UNIQUE (city, county, zipCode)
);

CREATE TABLE VetAvailability (
    availabilityID INT IDENTITY(1,1) PRIMARY KEY,
    vetID INT FOREIGN KEY REFERENCES Vet (vetID),
    startTime TIME,
    endTime TIME,
    charges DECIMAL(10, 2)
);
ALTER TABLE VetAvailability
ADD CONSTRAINT UC_ID_Charges UNIQUE (vetID, charges)

ALTER TABLE VetAvailability
ADD CONSTRAINT CHK_VetAvailability_StartEndTime CHECK (startTime < endTime);

ALTER TABLE VetAvailability
ADD CONSTRAINT CHK_VetAvailability_Charges CHECK (charges IS NOT NULL AND charges > 0);

CREATE TABLE Appointment (
    appointmentID INT IDENTITY(1,1) PRIMARY KEY,
	ownerID INT FOREIGN KEY REFERENCES Owner (ownerID),
    vetID INT FOREIGN KEY REFERENCES Vet (vetID),
	VetSpecialization NVARCHAR(50), 
    petID INT FOREIGN KEY REFERENCES Pet (petID),
	PetType NVARCHAR(50),
    AppointmentDate DATE,
    StartTime TIME,
    appStatus NVARCHAR(50), 
    reasonForVisit NVARCHAR(MAX),
);
ALTER TABLE Appointment
ADD CONSTRAINT UC_oID_vID UNIQUE (appointmentID,ownerID,vetID)


CREATE TABLE Labs (
    labID INT IDENTITY(1,1) PRIMARY KEY,
	labName VARCHAR(100),
    locationID INT FOREIGN KEY REFERENCES Location(locationID)
);


CREATE TABLE LabTests (
    labID INT FOREIGN KEY REFERENCES Labs(labID),
	testID INT IDENTITY (100,1) PRIMARY KEY,
    testName VARCHAR(100),
	testCost DECIMAL(10, 2),
	Constraint UC_ID_Name UNIQUE (testID, testName)
);
ALTER TABLE LabTests
ADD CONSTRAINT UC_testID_cost UNIQUE (testID, testCost)


CREATE TABLE LabTestBooked (
    bookingID INT IDENTITY(1,1) PRIMARY KEY,
    appointmentID INT FOREIGN KEY REFERENCES Appointment(appointmentID),
    petID INT FOREIGN KEY REFERENCES Pet(petID),
    testID INT FOREIGN KEY REFERENCES LabTests(testID),
	testName VARCHAR(100),
    labID INT FOREIGN KEY REFERENCES Labs(labID),
    testDate DATE,
    testResult VARCHAR(255),
	CONSTRAINT FK_testDetails FOREIGN KEY (testID, testName) REFERENCES LabTests (testID, testName)
);

ALTER TABLE LabTestBooked
ADD CONSTRAINT UC_testID_appID_booked UNIQUE (appointmentId, testID)

CREATE TABLE Medication (
    medicationID INT IDENTITY(1,1) PRIMARY KEY,
    appointmentID INT FOREIGN KEY REFERENCES Appointment(appointmentID),
	vetID INT,
	prescribedBy VARCHAR(100),
    petID INT FOREIGN KEY REFERENCES Pet(petID),
    medicationName VARCHAR(100),
    dosage_per_day VARCHAR(50),
    duration_in_days INT,
	date_prescribed DATE,
    CONSTRAINT FK_VetName_Pre FOREIGN KEY (vetID, prescribedBy) REFERENCES Vet(vetID,vetName)
);

CREATE TABLE Review (
    reviewID INT IDENTITY(1,1) PRIMARY KEY,
    vetID INT FOREIGN KEY REFERENCES Vet (vetID),
    appointmentID INT FOREIGN KEY REFERENCES Appointment (appointmentID),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    reviewText VARCHAR(255),
    reviewDate DATE,
    CONSTRAINT CHK_Review_Date CHECK (reviewDate <= GETDATE())
);

CREATE TABLE Payment (
    paymentID INT IDENTITY(1,1) PRIMARY KEY,
    appointmentID INT,
	ownerID INT,
	vetID INT,
    vetCharges DECIMAL(10, 2),
	testID INT,
    labTestCharges DECIMAL(10, 2),
    totalAmount AS (vetCharges + labTestCharges) PERSISTED,
    paymentDate DATE,
    CONSTRAINT CHK_Positive_VetCharges CHECK (vetCharges >= 0),
    CONSTRAINT CHK_Positive_LabTestCharges CHECK (labTestCharges >= 0),
    CONSTRAINT CHK_Positive_TotalAmount CHECK (totalAmount >= 0),
    CONSTRAINT FK_AppointmentID_Payment FOREIGN KEY (appointmentID, ownerID, vetID) REFERENCES Appointment(appointmentID,ownerID, vetID),
	CONSTRAINT FK_vetCharge FOREIGN KEY (vetID,vetCharges) REFERENCES VetAvailability (vetID, charges),
	CONSTRAINT FK_labCharge FOREIGN KEY (testID,labTestCharges) REFERENCES LabTests (testID, testcost)
);

select * from Appointment
select * from Payment
select * from Owner 
select * from Vet
select * from Pet where ownerID = 731
select * from Labs
select * from Location


select * from Medication where appointmentID = 10
select * from Review


select * from VetAvailability
select * from LabTestBooked
select * from LabTests

--Procedure for Adding a new Owner
CREATE PROCEDURE InsertOwner
    @fullName VARCHAR(100),
    @email VARCHAR(100),
    @phone VARCHAR(20),
    @city VARCHAR(50),
    @county VARCHAR(50),
    @zipCode VARCHAR(20),
    @regDate DATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Check if the city, county, and zipCode combination exists in Location table
    DECLARE @locationExists INT;
    SELECT @locationExists = COUNT(*) FROM Location WHERE city = @city AND county = @county AND zipCode = @zipCode;

    IF @locationExists > 0
    BEGIN
        -- Insert data into Owner table
        INSERT INTO Owner (fullName, email, phone, city, county, zipCode, regDate)
        VALUES (@fullName, @email, @phone, @city, @county, @zipCode, @regDate);

        SELECT 'Record inserted successfully' AS Result;
    END
    ELSE
    BEGIN
        SELECT 'Location does not exist in the Location table' AS Result;
    END
END;



-- Create a procedure to insert data into the Vet table
CREATE PROCEDURE InsertVetData
    @vetName VARCHAR(100),
    @specialization VARCHAR(100),
    @Email VARCHAR(100),
    @Phone VARCHAR(20),
    @city VARCHAR(50),
    @county VARCHAR(50),
    @zipCode VARCHAR(20),
    @IsCertified BIT,
    @regDate DATE
AS
BEGIN
    DECLARE @vetID INT

    -- Check if the city, county, and zipCode combination exists in the Location table
    IF EXISTS (SELECT 1 FROM Location WHERE city = @city AND county = @county AND zipCode = @zipCode)
    BEGIN
        -- Insert data into the Vet table
        INSERT INTO Vet (vetName, specialization, Email, Phone, city, county, zipCode, IsCertified, regDate)
        VALUES (@vetName, @specialization, @Email, @Phone, @city, @county, @zipCode, @IsCertified, @regDate)

        -- Get the newly inserted vetID
        SELECT @vetID = SCOPE_IDENTITY()

        -- Return the vetID of the newly inserted record
        SELECT @vetID AS 'InsertedVetID'
    END
    ELSE
    BEGIN
        -- If the city, county, and zipCode combination doesn't exist in Location table, return an error message
        PRINT 'Error: City, county, and zipCode combination does not exist in the Location table.'
    END
END;

CREATE PROCEDURE InsertPet
    @petName VARCHAR(50),
    @ownerID INT,
    @type VARCHAR(50),
    @breed VARCHAR(50),
    @DateOfBirth DATE,
    @petWeight DECIMAL(5, 2),
    @gender VARCHAR(10),
    @isVaccinated BIT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Pet (petName, ownerID, type, breed, DateOfBirth, petWeight, gender, isVaccinated)
    VALUES (@petName, @ownerID, @type, @breed, @DateOfBirth, @petWeight, @gender, @isVaccinated);
END;



CREATE PROCEDURE GetVetsBySpecialty
AS
BEGIN
    SELECT V.vetID, V.vetName, V.specialization
    FROM Vet as V
    INNER JOIN VetAvailability  as VA ON V.vetID = VA.vetID
    GROUP BY V.vetID, V.vetName, V.specialization
    ORDER BY V.specialization, V.vetName;
END;

CREATE PROCEDURE GetVetsByCost
AS
BEGIN
    SET NOCOUNT ON;

    SELECT v.vetID, v.vetName, v.specialization, v.city, v.county, v.zipCode, v.IsCertified, va.startTime, va.endTime, va.charges
    FROM Vet as v
    INNER JOIN VetAvailability as va ON v.vetID = va.vetID
    ORDER BY va.charges DESC;
END;


CREATE PROCEDURE GetVetsWithReviews
AS
BEGIN
    SELECT V.vetID, V.vetName, V.specialization, V.Email, V.Phone, V.city, V.county, V.zipCode, V.IsCertified, V.regDate,
           AVG(R.rating) AS AvgRating,
           COUNT(R.reviewID) AS TotalReviews
    FROM Vet as V
    LEFT JOIN Review as R ON V.vetID = R.vetID
    GROUP BY V.vetID, V.vetName, V.specialization, V.Email, V.Phone, V.city, V.county, V.zipCode, V.IsCertified, V.regDate
    ORDER BY AvgRating DESC;
END;



--Denormalized Table
SELECT 
    A.appointmentID,
    O.fullName AS OwnerName,
    O.email AS OwnerEmail,
    O.phone AS OwnerPhone,
    P.petName,
    P.type AS PetType,
    V.vetName AS VetName,
    V.specialization AS VetSpecialization,
	VA.charges AS VetFee,
    A.AppointmentDate,
    A.StartTime,
    A.appStatus AS AppointmentStatus,
    LT.testName AS LabTestName,
    LT.testCost AS LabTestCost,
    L.labName AS LabName,
    LB.testResult AS LabTestResult,
    M.medicationName,
    M.dosage_per_day AS Dosage,
    M.duration_in_days AS Duration,
    R.rating AS VetRating,
    R.reviewText AS VetReview
FROM Appointment as A
INNER JOIN Owner as O ON A.ownerID = O.ownerID
INNER JOIN Pet as P ON A.petID = P.petID
INNER JOIN Vet as V ON A.vetID = V.vetID
INNER JOIN VetAvailability as VA ON A.vetID = VA.vetID
LEFT JOIN LabTestBooked as LB ON A.appointmentID = LB.appointmentID
LEFT JOIN LabTests as LT ON LB.testID = LT.testID
LEFT JOIN Labs as L ON LB.labID = L.labID
LEFT JOIN Medication as M ON A.appointmentID = M.appointmentID
LEFT JOIN Review as R ON A.appointmentID = R.appointmentID;

CREATE TABLE ComprehensiveReport (
    appointmentID INT,
    OwnerName VARCHAR(100),
    OwnerEmail VARCHAR(100),
    OwnerPhone VARCHAR(30),
    PetName VARCHAR(50),
    PetType VARCHAR(50),
    VetName VARCHAR(100),
    VetSpecialization VARCHAR(100),
	VetFee DECIMAL(10, 2),
    AppointmentDate DATE,
    StartTime TIME,
    AppointmentStatus NVARCHAR(50),
    LabTestName VARCHAR(100),
    LabTestCost VARCHAR(50),
    LabName VARCHAR(100),
    LabTestResult VARCHAR(255),
    MedicationName VARCHAR(100),
    Dosage VARCHAR(50),
    Duration VARCHAR(50),
    VetRating VARCHAR(50),
    VetReview VARCHAR(255)
);
DROP table ComprehensiveReport

--INSERTION FROM CSV FILE
BULK INSERT ComprehensiveReport
FROM 'C:\CompTable.csv' 
WITH (
   FIELDTERMINATOR = ',',           
   ROWTERMINATOR = '\n',            
   FIRSTROW = 1                    
);



--VIEW
CREATE VIEW LocationDetailsView AS
SELECT L.city, L.county, L.zipCode,
       V.vetID AS VetID, V.vetName AS VetName, V.specialization AS VetSpecialization, V.Email AS VetEmail, V.Phone AS VetPhone,
       O.ownerID AS OwnerID, O.fullName AS OwnerName, O.email AS OwnerEmail, O.phone AS OwnerPhone
FROM Location as L
LEFT JOIN Vet as V ON L.city = V.city AND L.county = V.county AND L.zipCode = V.zipCode
LEFT JOIN Owner as O ON L.city = O.city AND L.county = O.county AND L.zipCode = O.zipCode;


--VIEW
CREATE VIEW PaymentSummaryView AS
SELECT P.paymentID, P.appointmentID, P.ownerID, P.vetID,
       P.vetCharges AS VetCharges, P.labTestCharges AS LabTestCharges,
       P.totalAmount AS TotalAmount,
       O.fullName AS OwnerName, O.email AS OwnerEmail, O.phone AS OwnerPhone,
       O.city AS OwnerCity, O.county AS OwnerCounty, O.zipCode AS OwnerZipCode
FROM Payment as P
JOIN Owner as O ON P.ownerID = O.ownerID;



CREATE VIEW TotalSpendingView AS
SELECT p.ownerID, o.fullName AS ownerFullName, o.email AS ownerEmail, o.phone AS ownerPhone,
       SUM(p.vetCharges) AS totalVetCharges, 
       SUM(p.labTestCharges) AS totalLabTestCharges, 
       SUM(p.totalAmount) AS totalAmountPaid
FROM Payment as p
INNER JOIN Owner as o ON p.ownerID = o.ownerID
GROUP BY p.ownerID, o.fullName, o.email, o.phone;


--AUDIT TABLE
CREATE TABLE AuditTrail (
    auditID INT IDENTITY(1,1) PRIMARY KEY,
    tableName NVARCHAR(100),
    action NVARCHAR(50),
    recordID INT,
    columnName NVARCHAR(100),
    oldValue NVARCHAR(MAX),
    newValue NVARCHAR(MAX),
    modifiedDate DATETIME DEFAULT GETDATE()
);

CREATE TRIGGER trg_VetSpecializationAudit
ON Vet
AFTER UPDATE
AS
BEGIN
    IF UPDATE(specialization)
    BEGIN
        DECLARE @oldValue NVARCHAR(MAX)
        DECLARE @newValue NVARCHAR(MAX)
        DECLARE @recordID INT

        SELECT @oldValue = deleted.specialization,
               @newValue = inserted.specialization,
               @recordID = inserted.vetID
        FROM inserted
        INNER JOIN deleted ON inserted.vetID = deleted.vetID

        INSERT INTO AuditTrail (tableName, action, recordID, columnName, oldValue, newValue)
        VALUES ('Vet', 'UPDATE', @recordID, 'specialization', @oldValue, @newValue)
    END
END;

--Trigger covering all columns of Vet
CREATE TRIGGER trg_VetAudit
ON Vet
AFTER UPDATE
AS
BEGIN
    IF UPDATE(specialization) OR UPDATE(vetName) OR UPDATE(Email) OR UPDATE(Phone) OR UPDATE(city) OR UPDATE(county) OR UPDATE(zipCode) OR UPDATE(IsCertified)
    BEGIN
        DECLARE @tableName NVARCHAR(100) = 'Vet'
        DECLARE @action NVARCHAR(50) = 'UPDATE'
        DECLARE @recordID INT
        SELECT @recordID = inserted.vetID FROM inserted

        DECLARE @columns TABLE (
            ColumnName NVARCHAR(100),
            OldValue NVARCHAR(MAX),
            NewValue NVARCHAR(MAX)
        )

        IF UPDATE(specialization)
        BEGIN
            DECLARE @oldSpecialization NVARCHAR(MAX)
            DECLARE @newSpecialization NVARCHAR(MAX)

            SELECT @oldSpecialization = deleted.specialization,
                   @newSpecialization = inserted.specialization
            FROM inserted
            INNER JOIN deleted ON inserted.vetID = deleted.vetID

            INSERT INTO @columns (ColumnName, OldValue, NewValue)
            VALUES ('specialization', @oldSpecialization, @newSpecialization)
        END
		IF UPDATE(vetName)
        BEGIN
            DECLARE @oldVetName NVARCHAR(100)
            DECLARE @newVetName NVARCHAR(100)

            SELECT @oldVetName = deleted.vetName,
                   @newVetName = inserted.vetName
            FROM inserted
            INNER JOIN deleted ON inserted.vetID = deleted.vetID

            INSERT INTO @columns (ColumnName, OldValue, NewValue)
            VALUES ('vetName', @oldVetName, @newVetName)
        END

        IF UPDATE(Email)
        BEGIN
            DECLARE @oldEmail NVARCHAR(100)
            DECLARE @newEmail NVARCHAR(100)

            SELECT @oldEmail = deleted.Email,
                   @newEmail = inserted.Email
            FROM inserted
            INNER JOIN deleted ON inserted.vetID = deleted.vetID

            INSERT INTO @columns (ColumnName, OldValue, NewValue)
            VALUES ('Email', @oldEmail, @newEmail)
        END

        IF UPDATE(Phone)
        BEGIN
            DECLARE @oldPhone NVARCHAR(20)
            DECLARE @newPhone NVARCHAR(20)

            SELECT @oldPhone = deleted.Phone,
                   @newPhone = inserted.Phone
            FROM inserted
            INNER JOIN deleted ON inserted.vetID = deleted.vetID

            INSERT INTO @columns (ColumnName, OldValue, NewValue)
            VALUES ('Phone', @oldPhone, @newPhone)
        END

		IF UPDATE(city) OR UPDATE(county) OR UPDATE(zipCode)
        BEGIN
            DECLARE @newCity NVARCHAR(50)
            DECLARE @newCounty NVARCHAR(50)
            DECLARE @newZipCode NVARCHAR(20)

            SELECT @newCity = inserted.city,
                   @newCounty = inserted.county,
                   @newZipCode = inserted.zipCode
            FROM inserted

            IF NOT EXISTS (SELECT * FROM Location WHERE city = @newCity AND county = @newCounty AND zipCode = @newZipCode)
            BEGIN
                RAISERROR ('Invalid combination of City, County, and ZipCode. It does not exist in the Location table.', 16, 1)
                ROLLBACK TRANSACTION
                RETURN
            END
        END

		IF UPDATE(IsCertified)
        BEGIN
            DECLARE @oldCerf NVARCHAR(100)
            DECLARE @newCerf NVARCHAR(100)

            SELECT @oldCerf = deleted.IsCertified,
                   @newCerf = inserted.IsCertified
            FROM inserted
            INNER JOIN deleted ON inserted.vetID = deleted.vetID

            INSERT INTO @columns (ColumnName, OldValue, NewValue)
            VALUES ('IsCertified', @oldCerf, @newCerf)
        END

        INSERT INTO AuditTrail (tableName, action, recordID, columnName, oldValue, newValue)
        SELECT @tableName, @action, @recordID, ColumnName, OldValue, NewValue
        FROM @columns
    END
END;


CREATE TRIGGER trg_OwnerUpdateAudit
ON Owner
AFTER UPDATE
AS
BEGIN
    IF UPDATE(fullName) OR UPDATE(email) OR UPDATE(phone) OR UPDATE(city) OR UPDATE(county) OR UPDATE(zipCode)
     BEGIN
        DECLARE @tableName NVARCHAR(100) = 'Owner'
        DECLARE @action NVARCHAR(50) = 'UPDATE'
        DECLARE @recordID INT
        SELECT @recordID = inserted.ownerID FROM inserted

        DECLARE @columns TABLE (
            ColumnName NVARCHAR(100),
            OldValue NVARCHAR(MAX),
            NewValue NVARCHAR(MAX)
        )

		IF UPDATE(fullName)
        BEGIN
            DECLARE @oldName NVARCHAR(20)
            DECLARE @newName NVARCHAR(20)

            SELECT @oldName = deleted.fullName,
                   @newName = inserted.fullName
            FROM inserted
            INNER JOIN deleted ON inserted.ownerID = deleted.ownerID

            INSERT INTO @columns (ColumnName, OldValue, NewValue)
            VALUES ('fullName', @oldName, @newName)
        END

		IF UPDATE(email)
        BEGIN
            DECLARE @oldEmail NVARCHAR(20)
            DECLARE @newEmail NVARCHAR(20)

            SELECT @oldEmail = deleted.email,
                   @newEmail = inserted.email
            FROM inserted
            INNER JOIN deleted ON inserted.ownerID = deleted.ownerID

            INSERT INTO @columns (ColumnName, OldValue, NewValue)
            VALUES ('email', @oldEmail, @newEmail)
        END

		IF UPDATE(phone)
        BEGIN
            DECLARE @oldPhone NVARCHAR(20)
            DECLARE @newPhone NVARCHAR(20)

            SELECT @oldPhone = deleted.phone,
                   @newPhone = inserted.phone
            FROM inserted
            INNER JOIN deleted ON inserted.ownerID = deleted.ownerID

            INSERT INTO @columns (ColumnName, OldValue, NewValue)
            VALUES ('phone', @oldPhone, @newPhone)
        END

		IF UPDATE(city) OR UPDATE(county) OR UPDATE(zipCode)
        BEGIN
            DECLARE @newCity NVARCHAR(50)
            DECLARE @newCounty NVARCHAR(50)
            DECLARE @newZipCode NVARCHAR(20)

            SELECT @newCity = inserted.city,
                   @newCounty = inserted.county,
                   @newZipCode = inserted.zipCode
            FROM inserted

            IF NOT EXISTS (SELECT * FROM Location WHERE city = @newCity AND county = @newCounty AND zipCode = @newZipCode)
            BEGIN
                RAISERROR ('Invalid combination of City, County, and ZipCode. It does not exist in the Location table.', 16, 1)
                ROLLBACK TRANSACTION
                RETURN
            END
        END

        INSERT INTO AuditTrail (tableName, action, recordID, columnName, oldValue, newValue)
        SELECT @tableName, @action, @recordID, ColumnName, OldValue, NewValue
        FROM @columns
    END
END;

--To find vet without any appointment
SELECT v.vetID, v.vetName
FROM Vet v
LEFT JOIN Appointment a ON v.vetID = a.vetID
WHERE a.appointmentID IS NULL;

--Insertion in Owner
INSERT INTO Owner (fullName, email, phone, city, county, zipCode, regDate)
VALUES ('Nadeem Rana', 'nadeemrana@gmail.com', '+44-456-78901', 'Rye', 'Sussex', '63687', GETDATE());


-- UPDATE operation in Audit
UPDATE Owner
SET fullName = 'Leo Smith', email = 'leo.smith@gmail.com'
WHERE ownerID = 731;
--Update Vet Specilization
UPDATE Vet
SET specialization = 'Canine'
WHERE vetID = 1525;

--AuditTrail Table
select * from AuditTrail

--Insertion Record for Vet
EXEC InsertVetData
    @vetName = 'Henry Steve', 
	@specialization = 'Canine', 
	@Email = 'henrys@yahoo.com', 
	@Phone = '+44-121-656545', 
    @city = 'Dover',
    @county = 'Kent',
    @zipCode = '84290',
	@IsCertified = 1, 
	@regDate = '2023-03-01';
--Insertion Record for Owner
EXEC InsertOwner 
    @fullName = 'John Doe',
    @email = 'johndoe@gmail.com',
    @phone = '+44-456-78901',
    @city = 'Dover',
    @county = 'Kent',
    @zipCode = '84290',
    @regDate = '2023-01-01';
-- Execute new pet in the Pet Table
EXEC InsertPet
    @petName = 'Buddy',
    @ownerID = 731, -- Replace with the actual owner ID
    @type = 'Dog',
    @breed = 'Golden Retriever',
    @DateOfBirth = '2019-05-15',
    @petWeight = 25.5,
    @gender = 'Male',
    @isVaccinated = 1;

-- Reports by Views
select * from [TotalSpendingView]
select * from [PaymentSummaryView]
select * from [LocationDetailsView]

-- Stored Procedures
EXEC GetVetsWithReviews;
EXEC GetVetsByCost;
EXEC GetVetsBySpecialty;

--To print Denormalized Table
select * from ComprehensiveReport;