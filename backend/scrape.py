import asyncio
import hashlib
from ai import ai_guess_delay
from playwright.async_api import async_playwright

# Función para extraer los tweets más recientes de un usuario de Twitter
# INPUT: "Twitter username"
# OUTPUT: [{"content": "Tweet content", "date": "Tweet date"}, ...]
async def fetch_recent_tweets(twitter_username):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="auth.json")
        page = await context.new_page()

        await page.goto("https://x.com/"+twitter_username)

        # Espera que los tweets se carguen
        await page.wait_for_selector('article')

        # Extrae el contenido de los tweets
        tweets = await page.evaluate('''
            () => {
                const tweet_elements = document.querySelectorAll('article');
                const tweets = [];
                tweet_elements.forEach(tweet => {
                    const content = tweet.querySelector('div[lang]')?.innerText;
                    const date = tweet.querySelector('time')?.getAttribute('datetime');
                    tweets.push({content, date})
                });
                return tweets;
            }
        ''')

        await browser.close()
        return tweets

def save_oficial_reports(conn):
    #target_username = "MetroCDMX"
    target_username = "TepalYael79389"

    cursor = conn.cursor()

    tweets = asyncio.run(fetch_recent_tweets(target_username))

    for tweet in tweets:
        tweet_hash = hashlib.sha256((tweet['content'] + tweet['date']).encode("utf-8")).hexdigest()

        # If the tweet was already saved, skip it
        cursor.execute("SELECT * FROM tweets_oficiales WHERE tweet_hash = ?", (tweet_hash,))
        if cursor.fetchone():
            continue

        # Print the new tweet
        print("New tweet:", tweet['content'])
        # Save the tweet in the database
        cursor.execute("INSERT INTO tweets_oficiales (tweet_hash) VALUES (?)", (tweet_hash,))

        list_of_delayed_lines = ai_guess_delay(tweet["content"])
        for line, delay in list_of_delayed_lines:
            s = f"datetime('now', '+{delay} minutes')"
            # The date will be the time the delay should stop
            cursor.execute("INSERT INTO reportes_usuario (usuario, linea, fecha) VALUES (0, ?, "+s+")", (line,))
            # Notify of new report
            print(f"New report: Line {line} will be delayed until {s}")

    conn.commit()

# Start scrapping every 15 minutes

from db import conexion_base_de_datos
import time

conn = conexion_base_de_datos()
print("Starting scraper")

while True:
    save_oficial_reports(conn)
    time.sleep(900)

