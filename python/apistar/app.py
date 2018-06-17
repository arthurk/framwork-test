import sys
import os

from apistar import App, ASyncApp, Route, exceptions, http

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from common import MemoryRepo  # noqa

repo = MemoryRepo()
repo.add_fixtures()

# def is_auth(password: str) -> bool:
#     return password == 'test'

async def list_articles() -> list:
    return repo.get_articles()

async def get_article(article_id: int) -> dict:
    try:
        article = repo.get_article(article_id)
    except LookupError:
        raise exceptions.NotFound()
    return article

async def create_article(app: App, data: http.RequestData,
                         password: http.Header) -> http.JSONResponse:
    # if not is_auth(password):
    #     raise exceptions.BadRequest()
    if not data['title']:
        raise exceptions.BadRequest()

    article_id = repo.add_article({'title': data['title']})
    url = app.reverse_url('get_article', article_id=article_id)
    headers = {'Location': url}
    return http.JSONResponse({}, status_code=201, headers=headers)

async def update_article(article_id: int, data: http.RequestData,
                         password: http.Header):
    # if not is_auth(password):
    #     raise exceptions.BadRequest()
    if not data['title']:
        raise exceptions.BadRequest()

    try:
        repo.update_article(article_id, data['title'])
    except LookupError:
        raise exceptions.NotFound()

async def delete_article(article_id: int, password: http.Header):
    # if not is_auth(password):
    #     raise exceptions.BadRequest()
    try:
        repo.delete_article(article_id)
    except LookupError:
        raise exceptions.NotFound()
    # JSONResponse will return invalid body + content-length
    # https://github.com/encode/apistar/issues/589
    return http.Response('', headers={'content-type': 'application/json'}, status_code=204)

routes = [
    Route('/articles', method='GET', handler=list_articles),
    Route('/articles/{article_id}', method='GET', handler=get_article),
    Route('/articles', method='POST', handler=create_article),
    Route('/articles/{article_id}', method='POST', handler=update_article),
    Route('/articles/{article_id}', method='DELETE', handler=delete_article),
]

app = ASyncApp(routes=routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 8000, debug=True)
