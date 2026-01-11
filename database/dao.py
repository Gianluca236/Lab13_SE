from database.DB_connect import DBConnect
from model.gene import Gene
from model.interazione import Interazione

class DAO:

    @staticmethod
    def get_geni():

        cnx = DBConnect.get_connection()

        result = {}

        if cnx is None:
            print("Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM gene"""
        try:
            cursor.execute(query)
            for row in cursor:
                gene = Gene(**row)
                result[gene.id] = gene
        except Exception as e:
            print(f"Errore durante la query get_tour: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_interazioni():

        cnx = DBConnect.get_connection()

        result = []

        if cnx is None:
            print("Errore di connessione al database.")
            return None

        cursor = cnx.cursor()
        query = """ SELECT *  FROM interazione"""
        try:
            cursor.execute(query)

            for row in cursor:
                interazione = Interazione(row[0],row[1],row[2],row[3])


                result.append(interazione)
        except Exception as e:
            print(f"Errore durante la query get_tour: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

