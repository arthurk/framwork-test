import sys
import os

from aiohttp import web

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from common import MemoryRepo  # noqa

repo = MemoryRepo()
repo.add_fixtures()

# FIXME: 500 errors return html
# other error codes return text/plain

# return json response for 404 (instead of text/plain)
@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.message
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
        message = ex.reason
    return web.json_response({'error': message}, status=404)

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
    article_id = repo.add_article({'title': data['title']})
    url = request.app.router['get_article'].url_for(id=str(article_id))
    headers = {'Location': str(url)}
    return web.json_response(status=201, headers=headers)

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
    return web.json_response(status=204)

app = web.Application(middlewares=[error_middleware])
app.add_routes([
    web.get('/articles', list_articles),
    web.get('/articles/{id:[0-9]+}', get_article, name='get_article'),
    web.post('/articles', create_article),
    web.post('/articles/{id:[0-9]+}', update_article),
    web.delete('/articles/{id:[0-9]+}', delete_article),
])

if __name__ == '__main__':
    # turn of access_log for performance reasons
    web.run_app(app, port=8000, access_log=None)
