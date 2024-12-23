import discogs_client
import time
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="music_label_data"
)

cursor = db.cursor()

token = "IVjLNDlEOpZSTjkQVZzjhBUQupJeZOhiEnGhyiww"
d = discogs_client.Client('ExampleApplication/0.1', token)




def get_label(id):
    for i in id:
        label = d.label(i)
        print(f"Label: {label.name}")
        get_releases(label)


def get_releases(label):
    num = label.releases.pages

    cursor.execute("INSERT IGNORE INTO label (label_name) VALUES(%s)", (label.name,))
    db.commit()

    cursor.execute("SELECT label_id FROM label WHERE label_name = %s", (label.name,))
    result = cursor.fetchone()
    label_id = int(result[0])
    while cursor.nextset():  # Закрываем открытые результаты
        pass

    for n in range(num):
        releases = label.releases.page(n)

        i = releases[0]


        # Выводим год релиза
        year = i.year if i.year != 0 else "Year not available"



        for r in releases:
            time.sleep(1)
            artist = str(r.artists[0].name)
            cursor.execute("INSERT IGNORE INTO author (author_name) VALUES(%s)", (artist,))
            db.commit()

            cursor.execute("SELECT author_id FROM author WHERE author_name = %s", (artist,))
            result = cursor.fetchone()
            artist_id = int(result[0])
            while cursor.nextset():  # Закрываем открытые результаты
                pass

            album_name = r.title
            time.sleep(1)



            if r.title != i.title and r.year:
                cursor.execute("INSERT INTO album (album_name, year, author_id, label_id) VALUES(%s, %s, %s, %s)", (album_name, r.year, artist_id, label_id))
                db.commit()

                cursor.execute("SELECT album_id FROM album WHERE album_name = %s", (r.title,))
                # time.sleep(1)
                album_id = int(cursor.fetchone()[0])
                while cursor.nextset():  # Закрываем открытые результаты
                    pass
                tracks = r.tracklist
                for tr in tracks:
                    time.sleep(0.5)
                    cursor.execute("INSERT INTO track (track_name, album_id) VALUES(%s, %s)", (tr.title, album_id))
                    db.commit()
                i = r


id = [42738]
get_label(id)

cursor.close()
db.close()