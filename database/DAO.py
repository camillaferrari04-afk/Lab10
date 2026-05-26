from database.DB_connect import DBConnect
from model.country import Country

from Lab02.dictionary import Dictionary


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getallcountries(year:int):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res=[]

        query = """select co.*
                    from contiguity c, country co
                    where c.state1no = co.CCode and c.year<=%s
                    group by c.state1no """

        cursor.execute(query,(year,))

        for row in cursor.fetchall():
            res.append(Country(**row))

        cursor.close()
        conn.close()

        return res

    @staticmethod
    def getedges(year: int):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []

        query = """select LEAST(c.state1no, c.state2no ) as naz1id,
                            GREATEST(c.state1no, c.state2no) as naz2id
                    from contiguity c
                    where c.year<=%s and conttype=1
                    group by naz1id, naz2id"""

        cursor.execute(query, (year,))

        for row in cursor.fetchall():
            res.append((row["naz1id"], row["naz2id"]))

        cursor.close()
        conn.close()

        return res
