import os
import httpx
import psycopg

def main():
    db_url = os.environ["DB_URL"]
    webhook = os.environ["SLACK_WEBHOOK"]

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT title, price, city, state, url
                FROM listings
                ORDER BY fetched_at DESC
                LIMIT 5
            """)
            rows = cur.fetchall()

    lines = []
    for title, price, city, state, url in rows:
        lines.append(f"- {title} | ${price:,} | {city}, {state} | {url}")

    msg = "*Housing Bot Digest (latest 5)*\n" + "\n".join(lines)
    httpx.post(webhook, json={"text": msg}, timeout=20).raise_for_status()
    print("Sent Slack digest.")

if __name__ == "__main__":
    main()
