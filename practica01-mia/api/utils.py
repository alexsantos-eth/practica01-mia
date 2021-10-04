# CLASE DE CONTROLADOR
class Controller:
    def __init__(self, app, service, cursor, connect):
        self.app = app
        self.cursor = cursor
        self.connect = connect
        self.service = service(cursor, connect)
        self.set_routes()

    # ASIGNAR RUTAS
    def set_routes(self):
        pass


# CLASE DE SERVICIO
class Service:
    def __init__(self, cursor, connect):
        self.cursor = cursor
        self.connect = connect
