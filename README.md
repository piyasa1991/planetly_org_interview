# Software engineering takeaway test

## How to build

cp
```bash
docker-compose build
```
## Prepare data loading
- Download the CSV file into a loction
- Open a terminal inside the project location
- Replace `PATH_TO_CSV_FILE` to your location

```bash
cp <PATH_TO_CSV_FILE> backend/interview_app/db/data/

```
## How to run and load data

```bash
docker-compose up
```
- Open another terminal and load the data
```bash
docker-compose run --rm backend python -m interview_app.db.data.load_data
```

- Data loading takes ~3 mins
- Run the application at http://0.0.0.0:8000/docs
- Interactive api docs is available at http://0.0.0.0:8000/docs
- openapi.json can be accessed from http://0.0.0.0:8000/openapi.json


## Run test cases (Optional)

```bash
docker-compose run backend pytest tests
```

## Examples
- Install curl
- Find the entry whose city has the highest AverageTemperature since the
year 2000.

Request:
```bash
curl -X 'GET' \
  'http://localhost:8000/cities/top/1?date_start=2000-01-01T00%3A00%3A00.000Z' \
  -H 'accept: application/json'
```

Response:
```bash
[
  {
    "city": "Ahvaz",
    "country": "Iran",
    "latitude": "31.35N",
    "longitude": "49.01E",
    "id": 43,
    "temperature": {
      "dt": "2013-07-01T00:00:00",
      "average_temperature": 39.15600000000001,
      "average_temperature_uncertainty": 0.37,
      "id": 120250
    }
  }
]
```
- Following above: assume the temperature observation of the city last month
breaks the record. It is 0.1 degree higher with the same uncertainty. Create
this entry.
Request:
```bash
curl -X 'POST' \
  'http://localhost:8000/cities/43/temperature' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "dt": "2022-02-01T00:00:00.000Z",
  "average_temperature": 39.256,
  "average_temperature_uncertainty": 0.1
}'
```

Response:
```bash
{
  "dt": "2022-02-01T00:00:00",
  "average_temperature": 39.256,
  "average_temperature_uncertainty": 0.1,
  "id": 8602476
}
```
- Following question 1: assume the returned entry has been found erroneous.
The actual average temperature of this entry is 2.5 degrees lower. Update
this entry.
Request:
```bash
curl -X 'PUT' \
  'http://localhost:8000/cities/43/temperature' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "dt": "2022-02-01T00:00:00.000Z",
  "average_temperature": 36.756,
  "average_temperature_uncertainty": 0
}'
```

Response:
```bash
{
  "dt": "2022-02-01T00:00:00",
  "average_temperature": 36.756,
  "average_temperature_uncertainty": 0,
  "id": 8602476
}
```

## Teardown

```bash
docker-compose down -v
```

It took me nearly 6 hours to work on this.
The challenge I had so far is to analyze the data and I have overcome it by simple
running sql queries for analysis.