import os
import psycopg

def main():
    db_url = os.environ["DB_URL"]

    listing = {
        "source": "sample",
        "source_id": "demo-1",
        "url": "https://example.com/demo-1",
        "title": "Demo listing in Nashua, NH",
        "price": 500000,
        "city": "Nashua",
        "state": "NH",
        "beds": 3,
        "baths": 2,
        "sqft": 1600,
        "description": "This is a demo listing inserted by the bot."
    }

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO listings (source, source_id, url, title, price, city, state, beds, baths, sqft, description)
                VALUES (%(source)s, %(source_id)s, %(url)s, %(title)s, %(price)s, %(city)s, %(state)s, %(beds)s, %(baths)s, %(sqft)s, %(description)s)
                ON CONFLICT (source, source_id) DO NOTHING
                """,
                listing
            )

    print("Inserted demo listing (if not already present).")

if __name__ == "__main__":
    main()
