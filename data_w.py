import sqlite3

conn = sqlite3.connect('recent_data.db')

c = conn.cursor()

# c.execute("""CREATE TABLE recent_cities (
#         city_name text,
#         city_icon text,
#         city_temp integer
#     )""")

# c.execute("INSERT INTO recent_cities VALUES ('Kraków', '456.png', 23)")

c.execute("SELECT * FROM recent_cities WHERE city_temp= 23")
print(c.fetchall())
conn.commit()




