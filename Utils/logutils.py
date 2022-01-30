class LogUtils:
    LOGGER = None

    @staticmethod
    def simple_log(*args):
        if LogUtils.LOGGER:
            LogUtils.LOGGER.log("Notes", " " + ",".join([str(a) for a in args]), concat=True)