import pandas as pd
import sqlite3

shop_csv = pd.read_csv('shop.csv')
track_csv = pd.read_csv('track.csv')

print(shop_csv.info())
print(track_csv.info())

con = sqlite3.connect('data.db')
cur = con.cursor()

# create shop information database
cur.execute(
            'CREATE TABLE IF NOT EXISTS shop (shop_id INT PRIMARY KEY, \
             name TEXT, location TEXT, category TEXT, luxury INT, people_in_shop INT,\
            opening_hours TEXT, description TEXT, commodity TEXT)'
            )

# create track information database
cur.execute(
            'CREATE TABLE IF NOT EXISTS track (track_id INT PRIMARY KEY, \
            user_id INT, visit_id INT, last_track_id INT, user_gender TEXT,\
            user_age INT, user_occupation TEXT)'
            )


# Insert data to database

for i in range(0, len(shop_csv)):
    print(i, shop_csv['shop_id'].iloc[i])
    sql =   'INSERT INTO shop (shop_id, name, location, category,\
            luxury, people_in_shop, opening_hours, description,\
            commodity) VALUES(? ,?, ?, ?, ?, ?, ?, ?, ?)'
    cur.execute(
            sql
            , (
                int(shop_csv['shop_id'].iloc[i])
                , shop_csv['name'].iloc[i]
                , shop_csv['location'].iloc[i]
                , shop_csv['category'].iloc[i]
                , int(shop_csv['luxury'].iloc[i])
                , shop_csv['people_in_shop'].iloc[i]
                , shop_csv['opening_hours'].iloc[i]
                , shop_csv['description'].iloc[i]
                , shop_csv['commodity'].iloc[i]
            )
        )
    con.commit()

for i in range(0, len(track_csv)):
    print(i, track_csv['track_id'].iloc[i])
    sql = 'INSERT INTO track (track_id, user_id, visit_id, last_track_id,\
            user_gender, user_age, user_occupation)\
             VALUES(? ,?, ?, ?, ?, ?, ?)'
    cur.execute(
            sql
            , (
                int(track_csv['track_id'].iloc[i])
                , int(track_csv['user_id'].iloc[i])
                , int(track_csv['visit_id'].iloc[i])
                , int(track_csv['last_track_id'].iloc[i])
                , track_csv['user_gender'].iloc[i]
                , int(track_csv['user_age'].iloc[i])
                , track_csv['user_occupation'].iloc[i]
            )
        )
    con.commit()


cur.execute("select * from shop")
print(cur.fetchall())

cur.execute("select * from track")
print(cur.fetchall())
con.close()
