import sqlite3

# Connect to sqlite 
connection = sqlite3.connect("student.db")

# Create a cursor obj to inser record, create table, retreive 
cursor = connection.cursor()

# Create the table 
table_info = """
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);

"""

cursor.execute(table_info)

# Insert some records 
cursor.execute('''Insert Into STUDENT values('Niall', 'Science', 'A', 90)''')
cursor.execute('''Insert Into STUDENT values('Louis', 'Maths', 'A', 94)''')
cursor.execute('''Insert Into STUDENT values('Liam', 'History', 'B', 97)''')
cursor.execute('''Insert Into STUDENT values('Harry', 'English', 'A', 90)''')
cursor.execute('''Insert Into STUDENT values('Zayn', 'Hindi', 'C', 50)''')


# Display records
print("The inserted records are")
data = cursor.execute('''SELECT * from STUDENT''')

for row in data:
    print(row)

# Close the connection 
connection.commit()
connection.close()


