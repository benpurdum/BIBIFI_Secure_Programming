-- USER CREATE

DELIMITER //
CREATE PROCEDURE insertUser (
    IN pUsername VARCHAR(50),
    IN pPassword VARCHAR(255),
    IN pRole VARCHAR(20),
    IN pName VARCHAR(100),
    IN pAge INT
)
BEGIN
    INSERT INTO Users (username, password, role)
    VALUES (pUsername, pPassword, pRole);

    INSERT INTO Persons (userID, name, age)
    VALUES (pUserID, pName, pAge);
END //
DELIMITER ;


-- EVENT CREATE
DELIMITER //
CREATE PROCEDURE createEvent (
    IN pTime TIME,
    IN pDate DATE,
    IN pRoom VARCHAR(100),
    IN pName VARCHAR(100)
)
BEGIN
    INSERT INTO GalleryEvents (time, date, room, name)
    VALUES (pTime, pDate, pRoom, pName);
END //
DELIMITER ;


-- EVENT HISTORY READ

DELIMITER //
CREATE PROCEDURE seeEventHistory ()
BEGIN
    SELECT *
    FROM GalleryEvents;
END //
DELIMITER ;


-- ROOM CREATE

DELIMITER //
CREATE PROCEDURE createRoom (
    IN pName VARCHAR(100),
    IN pNumPeople INT,
    IN pArt VARCHAR(255)
)
BEGIN
    INSERT INTO Rooms (name, numPeople, art)
    VALUES (pName, pNumPeople, pArt);
END //
DELIMITER ;


-- CHANGE ROOMS
DELIMITER //
CREATE PROCEDURE changeRooms (
    IN pUserID INT,
    IN pFromRoom VARCHAR(100),
    IN pToRoom VARCHAR(100),
    IN pTime TIME,
    IN pDate DATE
)
BEGIN
    UPDATE Rooms
    SET numPeople = numPeople - 1
    WHERE name = pFromRoom;

    UPDATE Rooms
    SET numPeople = numPeople + 1
    WHERE name = pToRoom;

    INSERT INTO AuditLogs (userID, time, date, fromRoom, toRoom)
    VALUES (pUserID, pTime, pDate, pFromRoom, pToRoom);
END //
DELIMITER ;


-- VIEW ALL ROOMS

DELIMITER //
CREATE PROCEDURE viewAllRooms ()
BEGIN
    SELECT *
    FROM Rooms;
END //
DELIMITER ;




