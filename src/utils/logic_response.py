


class logicResponse:

    def __init__(self, resultado, resultObj):
        self.status= resultado
        self.result= resultObj

    def get_status(self):
        return self.status
    def get_errorlog(self):
        return self.result