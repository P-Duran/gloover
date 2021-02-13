import gloover_ws.app


class Logger:
    @classmethod
    def log_warning(cls, msg: str):
        gloover_ws.app.application.logger.warning(msg)

    @classmethod
    def log_error(cls, msg: str):
        gloover_ws.app.application.logger.error(msg)

    @classmethod
    def log_debug(cls, msg: str):
        gloover_ws.app.application.logger.debug(msg)
