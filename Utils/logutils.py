class LogUtils:
    LOGGER = None

    @staticmethod
    def simple_log(*args):
        if LogUtils.LOGGER:
            LogUtils.LOGGER.log("Notes", " " + ",".join(args), concat=True)