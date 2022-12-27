from dotenv import dotenv_values

dotenvValues = dotenv_values("../.env")

config = {
    "apiUrl": dotenvValues["API_URL"],
    "apiKey": dotenvValues["API_KEY"],
    "botToken": dotenvValues["BOT_TOKEN"],
    "adminId": dotenvValues["ADMIN_ID"].split(","),
    "gameChan": dotenvValues["GAME_CHAN"].split(","),
    "cooldown_scout": dotenvValues["CD_SCOUT"],
    "cooldown_match": dotenvValues["CD_MATCH"],
    "ovrmax": dotenvValues["OVRMAX"],
    "match_hour": dotenvValues["MATCH_HOUR"],
    "targetChannel": dotenvValues["TARGET_CHANNEL"],
    "cupName": dotenvValues["CUP_NAME"],
    "dataPath": "../data/",
    "sharedRegistrationFilePath": "../../data/registrations.csv",
}
