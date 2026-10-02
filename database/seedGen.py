from random import randint
from werkzeug.security import generate_password_hash

names = ["Ben Purdum","Zoe Eigenbrod","Jacob Ford","Sean Shea","Will World","Ben Leber","Colin Grant","John Admin"]
usernames = ["bpurdum","zeigenbrod","jford","sshea","wworld","bleber","cgrant","admin"]
rooms = ["Gallery","Room 1","Room 2","Room 3","Lobby"]
art = ["Lots of Art","Art 1","Art 2","Art 3","Art L",]
eNames = ["Event 1","Event 2","Event 3"]
uID = 0
roles = ["Guest","Employee","Admin"]
dates = ["10/01/2026","10/02/2026","10/03/2026"]
times = ["12:30pm","1:30pm","2:30pm"]

sql = []

class People:
    def __init__(self, id, room):
        self.id = id
        self.room = room

people = []

#users/people
for i in range(len(names)):
    uID += 1
    role = roles[0]
    if i > 4 and i < 7:
        role = roles[1]
    elif i == 7:
        role = roles[2]
    room = rooms[randint(0,len(rooms)-1)]
    sql.append(f"insert into users values ('{uID}', '{usernames[i]}', '{generate_password_hash("password")}', '{role}')")
    sql.append(f"insert into persons ('{uID}', '{names[i]}', '{randint(18,30)}', '{room}')")
    people.append(People(uID,room))

#rooms
for i in range(len(rooms)):
    count = 0
    for p in people:
        if p.room == rooms[i]:
            count += 1
    sql.append(f"insert into rooms values ('{rooms[i]}', '{count}','{art[i]}')")

#galleryEvents
eID = 0
for i in range(3):
    eID += 1
    sql.append(f"insert into galleryEvents values ('{eID}', '{times[i]}', '{dates[i]}', '{rooms[randint(0,len(rooms)-2)]}', '{eNames[i]}')")

#auditLogs


#sessions and auditLogs
sID = 0
for i in people:
    sID += 1
    date = dates[randint(0,len(dates)-1)]
    sql.append(f"insert into sessions values ('{sID}', '{i.id}', '{times[0]}', '{date}', '{times[2]}', '{date}')")
    sql.append(f"insert into auditLogs values ('{i.id}', '{times[1]}'. '{date}'. '{rooms[4]}', '{i.room}')")

#write
if __name__ == "__main__":
    with open("seed.sql", "w") as f:
        for line in sql:
            f.write(line + "\n")

    print("seed.sql generated!")