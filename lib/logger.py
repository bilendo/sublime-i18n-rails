class Logger:
    @staticmethod
    def info(*args):
        print('[Rails I18n] [INFO]', *args)


    @staticmethod
    def warn(*args):
        print('[Rails I18n] [WARNING]', *args)
