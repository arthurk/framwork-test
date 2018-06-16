import sys
import os

from quart import Quart, Response, jsonify

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from common import MemoryRepo  # noqa

repo = MemoryRepo()
repo.add_fixtures()

app = Quart(__name__)

@app.route('/articles')
async def list_articles() -> Response:
    return jsonify(repo.get_articles())

if __name__ == '__main__':
    app.run(port=8000, debug=False)
