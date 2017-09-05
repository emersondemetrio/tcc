"""
Tracks Database Client
docs: https://github.com/PyMySQL/PyMySQL
"""

import pymysql.cursors
import util.utils as utils

class TracksDb:
    """Class TracksDb"""
    def get_connection(self, host="localhost", user="root", passwd="123", db_name="tcc_db"):
        """
        Get DB Connections
        """
        return pymysql.connect(
            host=host,
            user=user,
            password=passwd,
            db=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def truncate(self, table="all"):
        """Truncate given/all tables"""

        utils.show_message("Truncating %s table(s)." % table)

        sqls = []
        if table == "all":
            sqls.append("TRUNCATE table track_tags;")
            sqls.append("TRUNCATE table track;")
            sqls.append("TRUNCATE table tag;")
        else:
            sqls.append("TRUNCATE table %s;" % table)

        for sql in sqls:
            try:
                connection = self.get_connection()
                with connection.cursor() as cursor:
                    cursor.execute(sql)
            finally:
                connection.close()

    def insert_track(self, track):
        """Insert first track version"""

        sql = (
            "INSERT INTO `track` (`name`, `artist`, `album`, `path`, `modified`) "
            "VALUES (%s, %s, %s, %s, %s)"
        )

        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        track['track'],
                        track['artist'],
                        track['album'],
                        track['path'],
                        utils.get_cur_datetime()
                    )
                )
            connection.commit()
        finally:
            connection.close()

    def update_track(self, track_id, field, val):
        """Update track_id in field using val"""

        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                sql = "UPDATE `track` SET {} = '{}' WHERE `track`.id = {}".format(
                    field, val, track_id
                )
                #print(sql)
                cursor.execute(sql, ())
                connection.commit()
        finally:
            connection.close()

    def update_mbid(self, track, mbid):
        """Search and update mbid"""

        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT id FROM `track` WHERE name = (%s)"
                #print(sql)
                cursor.execute(sql, (track["track"],))

                try:
                    result = cursor.fetchone()
                    if result != None:
                        track_id = result['id']
                        print("Track: {}\nMBID: {}\n".format(track_id, mbid))
                        self.update_track(track_id, 'mbid', mbid)
                except AttributeError:
                    utils.show_message("Unable to update MIBD for %s" % track['track'], 1)

        finally:
            connection.close()

    def create_select_sql(self, fields, conditions, limit):
        """Create SELECT sql"""

        sql = "SELECT {} FROM `track` WHERE ".format(fields)
        where_condition = ""
        count = 0

        for condition in conditions:
            if count == 0:
                where_condition = "{} {}".format(
                    condition['field'],
                    condition['value']
                )
            else:
                where_condition = "{} AND {} {}".format(
                    where_condition,
                    condition['field'],
                    condition['value']
                )

            count = count + 1

        sql = "{} {} LIMIT {}".format(sql, where_condition, limit)
        return sql

    def get_tracks(self, fields="*", conditions=None, limit=300000):
        """Get All Tracks"""

        if conditions:
            sql = self.create_select_sql(fields, conditions, limit)
        else:
            sql = "SELECT {} FROM `track` LIMIT {}".format(fields, limit)

        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()
