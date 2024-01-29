import schedule
from Db_functions import DataBase


# schedule.every(1).day.at("09:00:00").do(DataBase().delete_after_time_good_end())
schedule.every(5).seconds.do(DataBase().delete_after_time_good_end)

while True:
    schedule.run_pending()
