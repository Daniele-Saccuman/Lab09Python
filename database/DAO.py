from database.DB_connect import DBConnect
from model.airline import Airline
from model.airport import Airport
from model.flight import Flight
from model.rotta import Rotta


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from airports a """

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllFlights():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from flights f """

        cursor.execute(query)

        for row in cursor:
            result.append(Flight(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllAirline():

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from airlines"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airline(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllRotte():

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select T1.ORIGIN_AIRPORT_ID as a1, T1.DESTINATION_AIRPORT_ID as a2, COALESCE(T1.D, 0) + COALESCE(T2.D, 0) as totDistance, COALESCE(T1.N, 0) + COALESCE(T2.N, 0) as nVoli
                    from
                    (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, sum(f.DISTANCE) as D, count(*) as N
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID ) as T1
                    left join 
                    (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, sum(f.DISTANCE) as D, count(*) as N
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID ) as T2
                    ON T1.ORIGIN_AIRPORT_ID = T2.DESTINATION_AIRPORT_ID AND T2.ORIGIN_AIRPORT_ID = T1.DESTINATION_AIRPORT_ID
                    WHERE T1.ORIGIN_AIRPORT_ID < T2.ORIGIN_AIRPORT_ID OR T2.ORIGIN_AIRPORT_ID IS NULL OR T2.DESTINATION_AIRPORT_ID IS NULL"""

        cursor.execute(query)

        for row in cursor:
            result.append(Rotta(**row))

        cursor.close()
        conn.close()
        return result
