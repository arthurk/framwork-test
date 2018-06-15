Implementation of the same project in different languages/frameworks.

A simple REST API that retrieves, creates, updates and deletes articles.

Article Resource Schema:
- id (int)
- title (string) required
- created (string: datetime in ISO8601 format)
- status (string: created, deleted)

The REST API should have the following Routes:

- GET /articles -> List all articles
- GET /articles/{id} -> Article details
- POST /articles -> create new article
- POST /articles/{id} -> update
- DELETE /articles/{id} -> delete

Notes:
- Exclude deleted articles
- Requests that modify data need to have authentication
- Make sure to return different error codes e.g. 400/404/405
- Creating an article should auto-increment the id
- Datetime should exclude microseconds
- Initial data with 3 articles should be available
