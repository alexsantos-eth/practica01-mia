# IMPORTS
from flask_cors import cross_origin
from api.utils import Controller


class data_controller(Controller):
    # DEFINIR RUTAS
    def set_routes(self):
        # SUBIR CSV
        @self.app.route('/cargarTemporal', methods=['POST'])
        @cross_origin()
        def upload_temporal():
            return self.service.upload_temporal()

        # CREAR MODELOS
        @self.app.route('/cargarModelo', methods=['POST'])
        @cross_origin()
        def set_data_model():
            return self.service.set_data_model()

        # BORRAR TEMPORAL
        @self.app.route('/eliminarTemporal', methods=['DELETE'])
        @cross_origin()
        def delete_temporal():
            return self.service.delete_temporal()

        # BORRAR MODELO
        @self.app.route('/eliminarModelo', methods=['DELETE'])
        @cross_origin()
        def delete_model():
            return self.service.delete_model()

        # CORRER CONSULTA 1
        @self.app.route('/consulta1', methods=['POST'])
        @cross_origin()
        def query_1():
            return self.service.run_query_n(1)

        # CORRER CONSULTA 2
        @self.app.route('/consulta2', methods=['POST'])
        @cross_origin()
        def query_2():
            return self.service.run_query_n(2)

        # CORRER CONSULTA 3
        @self.app.route('/consulta3', methods=['POST'])
        @cross_origin()
        def query_3():
            return self.service.run_query_n(3)

        # CORRER CONSULTA 4
        @self.app.route('/consulta4', methods=['POST'])
        @cross_origin()
        def query_4():
            return self.service.run_query_n(4)

        # CORRER CONSULTA 5
        @self.app.route('/consulta5', methods=['POST'])
        @cross_origin()
        def query_5():
            return self.service.run_query_n(5)

        # CORRER CONSULTA 6
        @self.app.route('/consulta6', methods=['POST'])
        @cross_origin()
        def query_6():
            return self.service.run_query_n(6)

            # CORRER CONSULTA 7
        @self.app.route('/consulta7', methods=['POST'])
        @cross_origin()
        def query_7():
            return self.service.run_query_n(7)

        # CORRER CONSULTA 8
        @self.app.route('/consulta8', methods=['POST'])
        @cross_origin()
        def query_8():
            return self.service.run_query_n(8)

        # CORRER CONSULTA 9
        @self.app.route('/consulta9', methods=['POST'])
        @cross_origin()
        def query_9():
            return self.service.run_query_n(9)

        # CORRER CONSULTA 10
        @self.app.route('/consulta10', methods=['POST'])
        @cross_origin()
        def query_10():
            return self.service.run_query_n(10)
