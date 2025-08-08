import sqlite3

##Connectionto sqlite

connection = sqlite3.connect("student.db")

#Create a cursor  object to insert,record, create table, and retrive

cursor =connection.cursor()


#Create table

table_info = """ 
Create table STUDENT (NAME VARCHAR(25) ,CLASS VARCHAR(25), 
SECTION VARCHAR(25), MARKS INT) """

cursor.execute(table_info)

#Insert more records

cursor.execute('''Insert Into STUDENT values ('Wazma', 'Data Science', 'A', 100)''')
cursor.execute('''Insert Into STUDENT values ('Ali', 'Artificial Intelligence', 'B', 80)''')
cursor.execute('''Insert Into STUDENT values ('Sana', 'Computer Science', 'C', 70)''')
cursor.execute('''Insert Into STUDENT values ('Safa', 'Medical Science', 'D', 60)''')
cursor.execute('''Insert Into STUDENT values ('Abubakr', 'GG Science', 'A', 90)''')


#display all the records 

print("Inserted records are: ")
data = cursor.execute('''Select * from STUDENT''')

for row in data:
    print(row)

#Close connection    
connection.commit()
connection.close()