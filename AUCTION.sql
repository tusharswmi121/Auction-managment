-- AUCTION;
USE AUCTION;

-- User Table
CREATE TABLE User (
    User_ID INT AUTO_INCREMENT Unique,
    Password VARCHAR(255) NOT NULL Unique,
    F_Name VARCHAR(255),
    M_Name VARCHAR(255),
    L_Name VARCHAR(255),
    Year_Of_Birth INT DEFAULT NULL,
    City VARCHAR(255) NOT NULL,
    Street VARCHAR(255) DEFAULT NULL,
    State VARCHAR(255) NOT NULL,
    Pincode INT NOT NULL,
    Email VARCHAR(255) NOT NULL CHECK (Email LIKE '%@%') Unique,
    PRIMARY KEY (User_ID)
);

-- Inserting data into User Table
INSERT INTO User (Username, Password, F_Name, M_Name, L_Name, Year_Of_Birth, City, Street, State, Pincode, Email)
VALUES
('john_doe', 'pass123', 'John', NULL, 'Doe', 1985, 'New York', '5th Ave', 'NY', 10001, 'john_doe@gmail.com'),
('jane_smith', 'pass456', 'Jane', NULL, 'Smith', 1990, 'Los Angeles', 'Main St', 'CA', 90001, 'jane_smith@gmail.com'),
('alex_brown', 'pass789', 'Alex', 'Michael', 'Brown', 1992, 'San Francisco', 'Market St', 'CA', 94105, 'alex_brown@gmail.com'),
('emily_jones', 'pass101', 'Emily', NULL, 'Jones', 1995, 'Chicago', 'Lake St', 'IL', 60601, 'emily_jones@gmail.com'),
('michael_green', 'pass102', 'Michael', NULL, 'Green', 1988, 'Miami', 'Ocean Dr', 'FL', 33101, 'michael_green@gmail.com'),
('linda_white', 'pass103', 'Linda', NULL, 'White', 1993, 'Boston', 'Beacon St', 'MA', 02108, 'linda_white@gmail.com'),
('kevin_wilson', 'pass104', 'Kevin', NULL, 'Wilson', 1986, 'Dallas', 'Elm St', 'TX', 75201, 'kevin_wilson@gmail.com'),
('sarah_clark', 'pass105', 'Sarah', NULL, 'Clark', 1991, 'Seattle', '1st Ave', 'WA', 98101, 'sarah_clark@gmail.com'),
('jason_king', 'pass106', 'Jason', NULL, 'King', 1984, 'Houston', 'Main St', 'TX', 77002, 'jason_king@gmail.com'),
('olivia_walker', 'pass107', 'Olivia', NULL, 'Walker', 1994, 'Denver', 'Colfax Ave', 'CO', 80202, 'olivia_walker@gmail.com');

-- User_Phone Table
CREATE TABLE User_Phone (
    User_ID INT,
    Phone VARCHAR(10) NOT NULL Unique,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE
);

-- Inserting data into User_Phone Table
INSERT INTO User_Phone (User_ID, Phone)
VALUES
(1, '1234567890'),
(2, '0987654321'),
(3, '1122334455'),
(4, '2233445566'),
(5, '3344556677'),
(6, '4455667788'),
(7, '5566778899'),
(8, '6677889900'),
(9, '7788990011'),
(10, '8899001122');

-- Seller Table
CREATE TABLE Seller (
    Seller_ID INT AUTO_INCREMENT Unique,
    User_ID INT UNIQUE,
    Username VARCHAR(255),
    Status VARCHAR(50),
    PRIMARY KEY (Seller_ID),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE
);

-- Inserting data into Seller Table
INSERT INTO Seller (User_ID, Username, Status)
VALUES
(1, 'john_doe', 'Active'),
(2, 'jane_smith', 'Active'),
(4, 'emily_jones', 'Active'),
(5, 'michael_green', 'Inactive'),
(7, 'kevin_wilson', 'Active');

-- Bidder Table
CREATE TABLE Bidder (
    Bidder_ID INT AUTO_INCREMENT Unique,
    User_ID INT UNIQUE,
    Username VARCHAR(255),
    Status VARCHAR(50) NOT NULL,
    PRIMARY KEY (Bidder_ID),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE
);

-- Inserting data into Bidder Table
INSERT INTO Bidder (User_ID, Username, Status)
VALUES
(2, 'jane_smith', 'Active'),
(3, 'alex_brown', 'Active'),
(6, 'linda_white', 'Active'),
(8, 'sarah_clark', 'Inactive'),
(9, 'jason_king', 'Active'),
(10, 'olivia_walker', 'Active');

-- Item Table
CREATE TABLE Item (
    Item_ID INT AUTO_INCREMENT,
    Seller_ID INT,
    Base_Price DECIMAL(10, 2),
    Description TEXT DEFAULT NULL,
    Status VARCHAR(50) NOT NULL,
    PRIMARY KEY (Item_ID),
    FOREIGN KEY (Seller_ID) REFERENCES Seller(Seller_ID) ON DELETE CASCADE
);



-- Inserting data into Item Table

-- Verify Seller_IDs in the Seller table to get the correct auto-increment values
/*
SELECT * FROM Seller;

-- Updated Item Table Insert (Make sure the Seller_ID exists)
INSERT INTO Item (Seller_ID, Base_Price, Description, Status)
VALUES
(1, 100.00, 'Vintage Watch', 'Available'),  -- john_doe
(2, 200.00, 'Antique Vase', 'Available'),   -- jane_smith
(3, 150.00, 'Old Camera', 'Available'),     -- emily_jones
(4, 500.00, 'Luxury Sofa', 'Unavailable'),  -- michael_green
(5, 300.00, 'Painting', 'Available');       -- kevin_wilson
*/


-- Bid Table
CREATE TABLE Bid (
    Bid_ID INT AUTO_INCREMENT,
    Item_ID INT,
    Amount DECIMAL(10, 2) NOT NULL,
    Status VARCHAR(50) NOT NULL,
    PRIMARY KEY (Bid_ID),
    FOREIGN KEY (Item_ID) REFERENCES Item(Item_ID) ON DELETE CASCADE
);

-- Inserting data into Bid Table
INSERT INTO Bid (Item_ID, Amount, Status)
VALUES
(1, 120.00, 'Valid'),
(2, 250.00, 'Valid'),
(3, 180.00, 'Valid'),
(4, 550.00, 'Valid'),
(5, 350.00, 'Valid');

-- Bidder_Bid Table
CREATE TABLE Bidder_Bid (
    Bidder_ID INT,
    Bid_ID INT,
    FOREIGN KEY (Bidder_ID) REFERENCES Bidder(Bidder_ID),
    FOREIGN KEY (Bid_ID) REFERENCES Bid(Bid_ID) ON DELETE CASCADE
);

-- Inserting data into Bidder_Bid Table
INSERT INTO Bidder_Bid (Bidder_ID, Bid_ID)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

-- Payment Table
CREATE TABLE Payment (
    Payment_ID INT AUTO_INCREMENT,
    Bid_ID INT,
    Amount DECIMAL(10, 2) NOT NULL,
    Mode_Of_Payment ENUM('UPI', 'COD', 'Net_Banking', 'Credit_Card'),
    PRIMARY KEY (Payment_ID),
    FOREIGN KEY (Bid_ID) REFERENCES Bid(Bid_ID) ON DELETE CASCADE
);

-- Inserting data into Payment Table
INSERT INTO Payment (Bid_ID, Amount, Mode_Of_Payment)
VALUES
(1, 120.00, 'UPI'),
(2, 250.00, 'Credit_Card'),
(3, 180.00, 'Net_Banking'),
(4, 550.00, 'UPI'),
(5, 350.00, 'COD');

-- Review Table
CREATE TABLE Review (
    Review_ID INT AUTO_INCREMENT,
    Bid_ID INT,
    Overview TEXT NOT NULL,
    Description TEXT DEFAULT NULL,
    PRIMARY KEY (Review_ID),
    FOREIGN KEY (Bid_ID) REFERENCES Bid(Bid_ID) ON DELETE CASCADE
);

-- Inserting data into Review Table
INSERT INTO Review (Bid_ID, Overview, Description)
VALUES
(1, 'Good Product', 'The vintage watch is in excellent condition.'),
(2, 'Amazing Piece', 'The antique vase was well worth the price.'),
(3, 'Decent', 'The old camera works fine.'),
(4, 'Excellent', 'The luxury sofa is of great quality.'),
(5, 'Beautiful Painting', 'The painting looks even better in real life.');




-- Displaying the table structures
DESCRIBE User;
DESCRIBE User_Phone;
DESCRIBE Seller;
DESCRIBE Bidder;
DESCRIBE Item;
DESCRIBE Bid;
DESCRIBE Bidder_Bid;
DESCRIBE Payment;
DESCRIBE Review;

-- DELETE FROM Seller;
DELETE FROM Bid;
DELETE FROM Bidder_Bid;
DELETE FROM  Review;


SELECT * FROM User;
SELECT * FROM User_Phone;
SELECT * FROM Seller;
SELECT * FROM Bidder;
SELECT * FROM Item;
SELECT * FROM Bid;
SELECT * FROM Bidder_Bid;
SELECT * FROM Payment;
SELECT * FROM Review;



-- Update the role of the user to admin 
-- UPDATE User SET Role = 'admin' WHERE Username = 'Tushar123';

-- Grant all privileges to the user Tushar123