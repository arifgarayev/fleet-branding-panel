from app.utils.utils import Utils
from app.model.keywords import Keywords


class KeywordsRepo:
    _session = None

    def set_session(self, db_session):
        if db_session:
            self._session = db_session

    def get_current_keyword(self):
        head_of_the_week = Utils.get_head_of_week()

        # FIXME please resume here
        return self._session.query(Keywords).filter_by(gen_date=head_of_the_week).all()


# if __name__ == '__main__':
#
#     import random
#     import datetime
#
#     i = 0
#     generated = []
#     while i < 50:
#
#         gen = random.randint(1000, 9999)
#
#         if gen not in generated:
#             generated.append(gen)
#             i += 1
#
#     start = datetime.datetime(2023, 11, 6)
#
#     for i in range(len(generated)):
#
#
#         # , start.strftime("%Y-%m-%d")
#         print(start.strftime("%Y-%m-%d"))
#
#         start += datetime.timedelta(days=7)
