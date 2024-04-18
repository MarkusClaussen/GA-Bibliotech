import mysql.connector

def låne_bok():
    try:
        # Kobler til databasen
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="hello",
            database="ga_bibliotek"
        )

        cursor = mydb.cursor()

        # Spør brukeren om ISBN og lånerens ID
        isbn = input("Skriv inn ISBN på boken du vil låne: ")
        lnr = input("Skriv inn lånerens ID: ")

        # Finn det første tilgjengelige eksemplaret for utlån
        cursor.execute("""
            SELECT EksNr 
            FROM eksemplar 
            WHERE ISBN = %s 
            AND EksNr NOT IN (
                SELECT EksNr FROM utlån
            )
            LIMIT 1
        """, (isbn,))
        eksemplar = cursor.fetchone()

        if eksemplar:
            eksnr = eksemplar[0]

            # Registrer utlånet i databasen
            cursor.execute("INSERT INTO utlån (LNr, ISBN, EksNr, Utlånsdato, Levert) VALUES (%s, %s, %s, CURDATE(), 0)",
                           (lnr, isbn, eksnr))
            mydb.commit()
            print("Boken er lånt ut.")
        else:
            print("Boken er ikke tilgjengelig for utlån.")
    except mysql.connector.Error as err:
        print("Feil ved låning av bok:", err)
    finally:
        if 'mydb' in locals() and mydb.is_connected():
            cursor.close()
            mydb.close()
            print("Databaseforbindelsen er lukket.")

# Bruk funksjonen
låne_bok()
