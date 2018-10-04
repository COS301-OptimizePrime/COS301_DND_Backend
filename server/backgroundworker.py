import datetime
import logging
import threading
import time

from sqlalchemy import and_

from . import db


class BackgroundWorker:
    logger = logging.getLogger("cos301-DND")

    conn = None

    def _connectDatabase(self):
        if not self.conn:
            self.conn = db.connect()

        return self.conn

    # Routine that processes whatever you want as background
    def BackgroundCleaner(self):
        try:
            while True:
                time.sleep(5)
                self.conn = self._connectDatabase()
                users = self.conn.query(db.User).filter(and_(
                    db.User.date_updated < datetime.datetime.now() - datetime.timedelta(
                        seconds=6), db.User.online == True))
                for _user in users:
                    _user.online = False
                    self.logger.info("User: " + _user.name + " is now inactive!")
                    self.conn.commit()
        except exc.SQLAlchemyError as err:
            self.logger.error("SQLAlchemyError! " + str(err))
        except Exception as err:
            self.logger.exception("Unhandled exception occurred! " + str(err))
        finally:
            self.conn.close()

    def start(self):
        t1 = threading.Thread(target=self.BackgroundCleaner)
        # Background thread will finish with the main program
        t1.setDaemon(True)
        t1.start()
        self.logger.debug("Started background worker!")
