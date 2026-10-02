BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "auditLogs" (
	"userID"	INTEGER,
	"time"	TEXT,
	"date"	TEXT,
	"fromRoom"	TEXT,
	"toRoom"	TEXT,
	PRIMARY KEY("userID")
);
CREATE TABLE IF NOT EXISTS "galleryEvents" (
	"eventID"	INTEGER,
	"time"	TEXT,
	"date"	TEXT,
	"room"	TEXT,
	"name"	TEXT,
	PRIMARY KEY("eventID")
);
CREATE TABLE IF NOT EXISTS "persons" (
	"userID"	INTEGER,
	"name"	TEXT,
	"age"	INTEGER,
    "currentRoom" TEXT,
	PRIMARY KEY("userID")
);
CREATE TABLE IF NOT EXISTS "rooms" (
	"name"	TEXT,
	"numPeople"	INTEGER,
	"art"	TEXT,
	PRIMARY KEY("name")
);
CREATE TABLE IF NOT EXISTS "sessions" (
	"sessionID"	INTEGER,
	"userID"	INTEGER,
	"loginTime"	TEXT,
	"loginDate"	TEXT,
	"logoutTime"	TEXT,
	"logoutDate"	TEXT,
	PRIMARY KEY("sessionID")
);
CREATE TABLE IF NOT EXISTS "users" (
	"userID"	INTEGER,
	"username"	TEXT,
	"password"	TEXT,
	"role"	TEXT,
	PRIMARY KEY("userID")
);
COMMIT;
