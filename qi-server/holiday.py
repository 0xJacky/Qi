# 节假日
import datetime


class Holiday:
    # 节假日
    holiday = [
        # 假期开始,放假天数
        '2020-10-01,8',
        '2021-01-01,3',
        # 2021 清明
        '2021-04-03,3',
        # 2021 劳动节
        '2021-04-30,7'
    ]

    # 生成节假日
    _holiday = []

    # 补课
    _makeup = {
        #   放假日         补课日
        '2020-10-07': '2020-09-27',
        '2020-10-08': '2020-10-10',
        '2021-05-04': '2021-04-25',
        '2021-05-05': '2021-05-08'
    }

    def __init__(self):
        for i in self.holiday:
            i = i.split(',')
            j = i[0].split('-')
            for k in range(0, int(i[1])):
                self._holiday += [
                    (datetime.datetime(int(j[0]), int(j[1]), int(j[2]))
                     + datetime.timedelta(days=float(k))).strftime('%Y-%m-%d')
                ]

    def is_holiday(self, date):
        return date in self._holiday

    def makeup(self, date):
        if date in self._makeup:
            j = self._makeup[date].split('-')
            return datetime.datetime(int(j[0]), int(j[1]), int(j[2]))
        return False
