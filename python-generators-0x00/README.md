# Seeding database

For the seed.py it is used to seed the database with initial data. The initial data can be downloaded by

```
wget -o user_data.csv <url-for-data>
```

## Streaming data

**Objective**: create a generator that streams rows from an SQL database one by one.

**Instructions**:

In 0-stream_users.py write a function that uses a generator to fetch rows one by one from the user_data table. You must use the Yield python generator

Prototype: def stream_users()
Your function should have no more than 1 loop
