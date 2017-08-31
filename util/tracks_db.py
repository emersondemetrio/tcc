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
