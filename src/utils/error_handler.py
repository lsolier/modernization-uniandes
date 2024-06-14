


class ErrorHandling(Exception):

    def __init__(self, estadoOperacion, detalleError):
        super().__init__()
        self._estadoOperacion = estadoOperacion
        self._detalleError= detalleError

    def __str__(self):
        return self.msg

    def get_estado(self):
        return self._estadoOperacion
    def get_detalle_error(self):
        return self._detalleError