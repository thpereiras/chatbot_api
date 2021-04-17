import os
from api import api

if __name__ == '__main__':
    api.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG", False),
        use_reloader=os.environ.get("DEBUG", False),
        threaded=True
    )
