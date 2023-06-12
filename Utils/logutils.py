class LogUtils:
    logger = None

    @classmethod
    def set_logger(cls, logger):
        cls.logger = logger

    @classmethod
    def simple_log(cls, *args):
        if cls.logger:
            cls.logger.log("Notes", " " + ",".join([str(a) for a in args]), concat=True)