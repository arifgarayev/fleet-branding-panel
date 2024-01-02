import datetime

import pytz


class Utils:

    @staticmethod
    def get_head_of_week():
        # convert servertime to AZT time

        baku_today = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Baku')).today()

        # print(baku_timezone_now)
        # print(type(baku_timezone_now))

        return (baku_today - datetime.timedelta(days=baku_today.weekday())).strftime("%Y-%m-%d")


if __name__ == '__main__':
    print(Utils.get_head_of_week())