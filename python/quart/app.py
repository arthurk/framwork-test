import sys
import os

from quart import Quart, Response, jsonify, request, exceptions

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from common import MemoryRepo  # noqa

repo = MemoryRepo()
repo.add_fixtures()

app = Quart(__name__)


# returns json on errors rather than html
class JsonException(exceptions.HTTPException):
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code

    def get_response(self) -> Response:
        return JsonResponse('', status=self.status_code)


class JsonResponse(Response):
    default_mimetype = 'application/json'


@app.route('/articles')
async def list_articles() -> Response:
    return jsonify(repo.get_articles())


@app.route('/articles/<int:article_id>')
async def get_article(article_id) -> Response:
    try:
        article = repo.get_article(article_id)
    except LookupError:
        raise JsonException(404)
    return jsonify(article)


@app.route('/articles', methods=['POST'])
async def create_article() -> Response:
    data = await request.get_json()
    print(data)
    if not data.get('title'):
        raise JsonException(400)

    article_id = repo.add_article({'title': data['title']})
    headers = {'Location': '/articles/%s' % article_id}
    return JsonResponse('', headers=headers, status=201)


@app.route('/articles/<int:article_id>', methods=['POST'])
async def update_article(article_id) -> Response:
    data = await request.get_json()
    if not data.get('title'):
        raise JsonException(400)
    try:
        repo.update_article(article_id, data['title'])
    except LookupError:
        raise JsonException(404)
    return JsonResponse('')


@app.route('/articles/<int:article_id>', methods=['DELETE'])
async def delete_article(article_id) -> Response:
    try:
        repo.delete_article(article_id)
    except LookupError:
        raise JsonException(404)
    return Response('', status=204)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
