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
                sql = "UPDATE `track` SET `{}` = '{}' WHERE `track`.id = {}".format(
                    field, val, track_id,
                )
                cursor.execute(sql)
        finally:
            connection.close()

    def update_mbid(self, track, mbid):
        """Search and update mbid"""

        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT id FROM `track` WHERE name = (%s)"
                cursor.execute(sql, (track["track"]))

                try:
                    self.update_track(cursor.fetchone()['id'], 'mbid', mbid)
                except AttributeError:
                    utils.show_message("Unable to update MIBD for %s" % track['track'], 1)

        finally:
            connection.close()

    def get_tracks(self, limit=300000):
        """Get All Tracks"""

        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `track` LIMIT (%s)"
                cursor.execute(sql, (limit))
                return cursor.fetchall()
        finally:
            connection.close()
