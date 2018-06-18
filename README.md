A simple REST API that retrieves, creates, updates and deletes articles.

Article Resource Schema:
- id (int)
- title (string)
- created (string: datetime in ISO8601 format)
- status (string: created|deleted)

The REST API should have the following Routes:

- GET /articles -> List all articles
- GET /articles/{id} -> Article details
- POST /articles -> create new article
- POST /articles/{id} -> update
- DELETE /articles/{id} -> delete

Load Testing
------------

Load testing is done with [k6](https://github.com/loadimpact/k6) which runs
virtual users who follow this script:

1. Create a new article
2. Retrieve the article
3. Update the article
4. Get the article (to make sure the update was successful)
5. Delete the article
6. Get the article (to make sure it was deleted)

Check `benchmark/script.js` for details.
