import mysql.connector
from datetime import datetime, timedelta

def sjekk_purring(email):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="hello",
            database="ga_bibliotek"
        )

        cursor = mydb.cursor()

        # Finn LNr for den gitte e-postadressen
        cursor.execute("SELECT LNr FROM låner WHERE Epost = %s", (email,))
        result = cursor.fetchone()

        if result:
            lnr = result[0]

            # Finn alle utlån for denne brukeren som er mer enn 14 dager gammel og ikke returnert
            today = datetime.now()
            fourteen_days_ago = today - timedelta(days=14)
            cursor.execute("SELECT bok.Tittel FROM utlån "
                           "JOIN bok ON utlån.ISBN = bok.ISBN "
                           "WHERE utlån.LNr = %s AND utlån.Utlånsdato <= %s AND utlån.Levert = 0", (lnr, fourteen_days_ago))
            purringer = cursor.fetchall()

            if purringer:
                for purring in purringer:
                    book_title = purring[0]
                    print(f"Send purring til {email}: Du har lånt boken '{book_title}' i over 14 dager.")

            else:
                print(f"Ingen purringer å sende for {email}.")

        else:
            print(f"Ingen bruker funnet med e-postadressen {email}.")

    except mysql.connector.Error as err:
        print("Feil ved purring:", err)

    finally:
        if 'mydb' in locals() and mydb.is_connected():
            cursor.close()
            mydb.close()
            print("Databaseforbindelsen er lukket.")

# Brukerinput for e-postadressen som skal sjekkes
email = input("Skriv inn e-postadressen du vil sjekke for purringer: ")
sjekk_purring(email)