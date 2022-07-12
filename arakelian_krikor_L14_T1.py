import sqlite3
import csv
import sys

# Connect to the database and set the cursor
con = sqlite3.connect("farakelian_krikor-food.db")
cur = con.cursor()

# Create the table
try:
    cur.execute("CREATE TABLE food(code STR, descript STR, nmbr INT, nutname STR, retention INT)")
except sqlite3.OperationalError:
    pass

# Read the file and parse the data
with open("retn5_dat.txt", "r") as input_file:
    data = []
    for row in csv.reader(input_file, delimiter="^"):
        code = row[0][1:-1]
        descript = row[1][1:-1]
        nmbr = row[2][1:-1]
        nutname = row[3][1:-1]
        retention = row[4][1:-1]
        data.append([code, descript, nmbr, nutname, retention])
for entry in data:
    cur.execute("INSERT INTO food(code, descript, nmbr, nutname, retention) VALUES(?, ?, ?, ?, ?)", entry)
con.commit()  # Commit the data to the table

# Execute and print command line parameter
cur.execute(sys.argv[1])
print(cur.fetchone())
# Close the database
con.close()
