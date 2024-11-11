#!./bin/python
import csv
import argparse
import logging
import psycopg2

# Define constants
TABLE_NAME = 'YOUR_TABLE_NAME'
HOST = 'localhost'
PORT = 5432
USER = 'YOUR_PG_USERNAME'
PASSWORD = 'YOUR_PG_PASSWORD'
DBNAME = 'YOUR_DB_NAME'

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Import CSV into PostgreSQL')
    parser.add_argument('-c', '--csv', required=True, help='Path to CSV file')

    return parser.parse_args()

def create_table(conn):
    """Create table if not exists."""
    query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            Date DATE,
            Reason VARCHAR(255),
            Amount NUMERIC(10, 2),
            Credit BOOLEAN,
            Category VARCHAR(255),
            PRIMARY KEY (Date, Reason, Amount, Credit)
        );
    """
    with conn.cursor() as cur:
        cur.execute(query)

def insert_records(conn, records):
    """Insert records into PostgreSQL table."""
    query = f"""
        INSERT INTO {TABLE_NAME} (Date, Reason, Amount, Credit, Category)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (Date, Reason, Amount, Credit) DO NOTHING;
    """
    with conn.cursor() as cur:
        for record in records:
            try:
                Amount = float(record[2])
                Credit = record[3].lower() == 'true'
                Category = record[4]
                cur.execute(query, (record[0], record[1], Amount, Credit, Category))
            except ValueError as e:
                logging.warning(f"Invalid value: {e}")

def main():
    args = parse_arguments()

    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname=DBNAME
        )
    except psycopg2.Error as e:
        logging.fatal(f"Connection failed: {e}")
        return

    # Read CSV file
    try:
        with open(args.csv, 'r') as csv_file:
            reader = csv.reader(csv_file)
            records = list(reader)
    except FileNotFoundError:
        logging.fatal(f"File not found: {args.csv}")
        return

    # Skip header row if present
    if records:
        records = records[1:]

    create_table(conn)
    insert_records(conn, records)
    conn.commit()

    logging.info("Data inserted successfully.")
    conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
