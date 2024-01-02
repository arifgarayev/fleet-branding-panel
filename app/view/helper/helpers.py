


class HelperUtils:

    @staticmethod
    def try_or_default(fn,
                       default_value):

        try:
            return fn()
        except Exception as e:
            print(e)
            return default_value
