# Challenge: User service
The objective of this exercise is to implement a rest-service which is able to:

- Create new user with contact data
- Return user by id
- Return user by name
- Add additional mail/phone data
- Update existing mail/phone data
- Delete user

## How to build

cp
```bash
docker-compose build
```

## How to run

```bash
docker-compose up
```

- Run the application at http://0.0.0.0:8000/docs
- Interactive api docs is available at http://0.0.0.0:8000/docs
- openapi.json can be accessed from http://0.0.0.0:8000/openapi.json
- Data is stored in Postgres


## Load data
```bash
docker-compose run --rm backend python -m interview_app.db.data.load_data
```

- Data loading takes ~3 mins


## Run test cases

```bash
docker-compose run backend pytest tests
```


## Examples
1.


## Teardown

```bash
docker-compose down
```