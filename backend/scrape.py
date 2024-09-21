import asyncio
import hashlib
from playwright.async_api import async_playwright
from openai import OpenAI
import sqlite3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../api'))
import db

client = OpenAI()

def ai_guess_delay(message) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "The following message is a tweet from a official subway account. Please, if the message is that a subway line or lines are delayed (now or in the future, ignore if it was in the past), return an array of lines and the estimated delay in minutes if no time is given try to guess a number on the range from 1 to 60 minutes, otherwise return an empty array and 0 minutes. People who fall to the rails cause a delay of no less than 30 minutes. The response should be in raw json format, no markdown, only json. There lines are 1-9, A,B and 12 The attributes are 'lines' and 'delay'."},
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return completion.choices[0].message.content

async def login_to_twitter(page, username, password):
    # Navega a la página de inicio de sesión de Twitter
    await page.goto('https://twitter.com/login')

    # Espera a que los campos de inicio de sesión se carguen y rellénalos
    await page.fill('input[type="text"]', username)

    botones = await page.query_selector_all('button')

    await botones[-2].click()

    await page.fill('input[type="text"]', password)

    botones = await page.query_selector_all('button')

    await botones[-1].click()

    # Espera a que se complete la navegación y se cargue la página principal de Twitter
    # await page.wait_for_navigation()

async def fetch_recent_tweets(username, twitter_username, twitter_password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="auth.json")
        page = await context.new_page()

        # await page.goto("https://x.com/MetroCDMX")
        await page.goto("https://x.com/TepalYael79389")

        # # Inicia sesión en Twitter
        # await login_to_twitter(page, twitter_username, twitter_password)

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

# Reemplaza 'usuario_de_twitter' con el nombre de usuario de Twitter que deseas consultar
target_username = 'MetroCDMX'

# Credenciales de tu cuenta de Twitter
twitter_username = 'TepalYael79389'
twitter_password = 'Hans66306713333'

tweets = asyncio.run(fetch_recent_tweets(target_username, twitter_username, twitter_password))
print(tweets)
for tweet in tweets:
    tweethash = hashlib.sha256((tweet['content'] + tweet['date']).encode("utf-8")).hexdigest()
    print(tweet["content"], "\n", ai_guess_delay(tweet["content"]))
    # Guarda un nuevo reporte en la base de datos
    conn = db.conexion_base_de_datos()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conexiones")
    print('HUH', cursor.fetchall())
    
    #inserta rn la base de datos metro.deb los tweets en la tabla reporte_lineas con el hash del tweet y el contenido del tweet
    #cursor.execute("INSERT INTO reporte_lineas (hash, contenido) VALUES (?, ?)", (tweethash, tweet["content"]))
    #conn.commit()
    #conn.close()
    
    #agregar usuarios a la base de datos desde el fronted
    #cursor.execute("INSERT INTO usuarios (nombre, correo, contraseña) VALUES (?, ?, ?)", (nombre, correo, contraseña))
    #conn.commit()
    #conn.close()
    #cursor.execute("SELECT * FROM usuarios")
    #print(cursor.fetchall())
    
    