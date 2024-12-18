HOWTO start everything up:

1. Clone and activate venv for all the libraries
2. Download pgadmin adn learn how to set up postgresql server (or find a setup)
3. Run the main file using "uvicorn main:app --reload"
4. Profit!😎

TODOs:

1. Fix the deprecated get_items (probably pydantic module issue or skill issue 😢 in async, tbd
2. Add authorization and authentication (involves jwt, another db table with login, hashed passwords, etc)
3. Add caching using Redis or Rabbitmq
4. Dockerize everything
