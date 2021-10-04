# IMPORTAR ENDPOINTS
from api.core import PSQLApi

# INICIAR API
app = PSQLApi()

# INICIAR API
if __name__ == "__main__":
    app.run(host='0.0.0.0')
