
# The Portfolio API  (www.theportfolioapi.com)

The Portfolio (REST) API is for wealth advisers and personal investors to screen investments across multiple asset classes, generate quantitative and qualitative analyses of these assets, and construct optimised investment portfolios.


## API Documentation

[Swagger Format Documentation](www.theportfolioapi.com)

[ReDoc Format Documentation](www.theportfolioapi.com/docs)
  
## Usage/Examples

Register as a new user:
```
curl -X 'POST' \
  'http://theportfolioapi.com/api/authentication/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "new_user": {
    "email": "user@example.com",
    "password": "password123",
    "username": "password123"
  }
}'
```

Login and receive JWT Bearer token:

```
curl -X 'POST' \
  'http://theportfolioapi.com/api/authentication/login/token/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=user%40example.com&password=strings'
```

Screen equities in the United States and in the Technology sector:  
```
curl -X 'GET' \
  'http://theportfolioapi.com/api/screener/equities/?sectors=Technology&industries=string&countries=United%20States' \
  -H 'accept: application/json'
  -H 'Authorization: Bearer $access_token'
```
Authorization must be formatted as 'Bearer' followed by your token.
## Run Locally

Clone the project

```bash
  git clone https://github.com/moebourji/theportfolioapi.git
```

Go to the project directory

```bash
  cd theportfolioapi
```

Start the server

```bash
  docker-compose up --build
```

  
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`

`POSTGRES_USER`

`POSTGRES_PASSWORD`

`POSTGRES_SERVER`

`POSTGRES_PORT`

`POSTGRES_DB`
  
## Roadmap

- Additional types of quantiative and qualitative analyses under the Analysis endpoint.

- More tests.

  
## Tech Stack

**Programming Language:** Python 3.8

**Backend Framework:** FastAPI

**Database:** PostgreSQL, SQLAlchemy, alembic

**Deployment**: Docker, Heroku

**Testing**: pytest, httpx

**Core Libraries:** pandas, scipy/numpy, bokeh, yfinance, yahooquery, pyjwt, passlib
  
## Appendix

This is a prototype project in early stages of development and should not be used to make any financial decisions.

  
## License

[MIT](https://choosealicense.com/licenses/mit/)

  
## Authors

- [@moebourji](https://github.com/moebourji)

  