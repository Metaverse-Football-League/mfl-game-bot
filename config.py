from dotenv import dotenv_values

dotenvValues = dotenv_values(".env")

config = {
    "apiUrl": dotenvValues["API_URL"],
    "apiKey": dotenvValues["API_KEY"],
    "botToken": dotenvValues["BOT_TOKEN"],
}
