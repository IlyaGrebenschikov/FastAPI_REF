# FastAPI Referral application itegrated with Redis, PostgreSQL and SQLAlchemy
About:

`Fully async application, user registration and authentication (JWT, Oauth 2.0).`

`An authenticated user has the opportunity to create or delete his referral code, which is stored in the Redis storage.`

`Possibility of receiving a referral code by email address of the referrer.`

`Possibility of registering using a referral code as a referral.`

`Obtaining information about referrals by referrer id.`

`UI documentation (Swagger/ReDoc).`

Setup:

`docker compose -f docker-compose.yaml up`

Env-file:

`You need to rename .env_example to .env and set your values.`

`POSTGRES_HOST=host`

`POSTGRES_PORT=port`

`POSTGRES_USER=username`

`POSTGRES_PASSWORD=password`

`POSTGRES_DB=dbname`

`DB_URL='postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'`