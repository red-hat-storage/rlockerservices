class ServiceBase:
    def run(self):
        """
        Decide the action the service needs to do repetitively, based
            on some interval time that will be passed by a YAML configuration file
        :return: None
        """
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __enter__(self):
        pass
