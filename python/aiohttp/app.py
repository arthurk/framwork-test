import sys
import os

from aiohttp import web

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from common import MemoryRepo  # noqa

repo = MemoryRepo()
repo.add_fixtures()

async def list_articles(request):
    return web.json_response(repo.get_articles())

async def get_article(request):
    article_id = int(request.match_info['id'])
    try:
        article = repo.get_article(article_id)
    except LookupError:
        raise web.HTTPNotFound()
    return web.json_response(article)

async def create_article(request):
    data = await request.json()
    if data['title'] == '':
        return web.HTTPBadRequest()

    repo.add_article({'title': data['title']})
    return web.json_response()

async def update_article(request):
    data = await request.json()
    if data['title'] == '':
        return web.HTTPBadRequest()

    article_id = int(request.match_info['id'])
    try:
        repo.update_article(article_id, data['title'])
    except LookupError:
        raise web.HTTPNotFound()
    return web.json_response()

async def delete_article(request):
    article_id = int(request.match_info['id'])
    try:
        repo.delete_article(article_id)
    except LookupError:
        raise web.HTTPNotFound()
    return web.json_response()

app = web.Application()
app.add_routes([
    web.get('/articles', list_articles),
    web.get('/articles/{id:[0-9]+}', get_article),
    web.post('/articles', create_article),
    web.post('/articles/{id:[0-9]+}', update_article),
    web.delete('/articles/{id:[0-9]+}', delete_article),
])

if __name__ == '__main__':
    web.run_app(app, port=8000, access_log=None)
