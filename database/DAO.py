from database.DB_connect import DBConnect
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                    FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                       FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllChrom():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                select distinct g.Chromosome
                from genes g
                order by g.Chromosome 
            """
            cursor.execute(query)

            for row in cursor:
                result.append(row["Chromosome"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllGenesByChrom(chromMin, chromMax):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                    select * 
                    from genes g
                    where g.Chromosome >= %s and g.Chromosome <= %s
            """
            cursor.execute(query, (chromMin, chromMax))

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(chromMin, chromMax):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                    select t1.geneid as gen1, t1.`Function` as f1, t2.geneid as gen2, t2.`Function` as f2,  i.Expression_Corr as peso
                    from 
                    (
                            select g.GeneID, g.Chromosome, c.Localization, g.`Function`
                            from genes g, classification c 
                            where g.Chromosome >= %s and g.Chromosome <= %s and c.GeneID = g.GeneID 
                    ) as t1,
                    (
                            select g.GeneID, g.Chromosome, c.Localization, g.`Function` 
                            from genes g, classification c 
                            where g.Chromosome >= %s and g.Chromosome <= %s and c.GeneID = g.GeneID 
                    ) as t2,
                    interactions i 
                    where t1.GeneID < t2.GeneID and t1.Localization = t2.Localization and 
                    ((t1.geneid = i.GeneID1 and t2.geneid = i.GeneID2) or (t1.geneid = i.GeneID2 and t2.geneid = i.GeneID1))
            """
            cursor.execute(query, (chromMin, chromMax, chromMin, chromMax))

            for row in cursor:
                result.append((row["gen1"], row["f1"], row["gen2"], row["f2"], row["peso"]))

            cursor.close()
            cnx.close()
        return result