import mysql.connector


# Funksjon for å slette en bok basert på ISBN
def slett_bok(cursor, isbn):
    try:
        # Hent alle EksNr for den aktuelle boken
        cursor.execute("SELECT EksNr FROM eksemplar WHERE ISBN = %s", (isbn,))
        eksnr_result = cursor.fetchall()
        eksnr_list = [eks[0] for eks in eksnr_result]

        # Slett relaterte utlån basert på EksNr
        for eksnr in eksnr_list:
            cursor.execute("DELETE FROM utlån WHERE EksNr = %s", (eksnr,))

        # Slett eksemplarer av den aktuelle boken
        cursor.execute("DELETE FROM eksemplar WHERE ISBN = %s", (isbn,))

        # Til slutt, slett boken selv
        cursor.execute("DELETE FROM bok WHERE ISBN = %s", (isbn,))

        print(f"Boken med ISBN {isbn} er slettet.")
    except mysql.connector.Error as err:
        print("Feil ved sletting av bok:", err)


# Koble til MySQL-databasen
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hello",
        database="ga_bibliotek"
    )

    if mydb.is_connected():
        print("Koblet til MySQL-databasen")

        cursor = mydb.cursor()

        # Input fra brukeren
        isbn = input("Skriv inn ISBN til boken du vil slette: ")
        slett_bok(cursor, isbn)

        mydb.commit()
        cursor.close()
except mysql.connector.Error as err:
    print("Feil ved tilkobling til MySQL-databasen:", err)
finally:
    if mydb.is_connected():
        mydb.close()
        print("Tilkoblingen til MySQL-databasen er lukket")
