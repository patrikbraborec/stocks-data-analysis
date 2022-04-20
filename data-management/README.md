# Data Management

## How to start

1. Start `PostgreSQL` and `GoodData.CN`:

```bash
$ docker-compose up
```

2. Run Python scripts to load, calculate and insert all data to `PostgreSQL`:

```bash
$ python3 ./src/main.py
```

---

To connect data source (PostgreSQL) to GoodData.CN, run the script with `-d` argument:

```bash
$ python3 ./src/main.py -d=True
```