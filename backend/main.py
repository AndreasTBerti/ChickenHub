from fastapi import FastAPI, HTTPException
import httpx
import time

from models.model import SensorData

app = FastAPI()

API_KEY = "ACESS_KEY_API"
THINGSPEAK_API_KEY = "4Q29CCRIUG8OAR22"

INTERVALO_MINIMO_DE_TEMPO = 20
ultimo_envio = {}
def pode_enviar(id_sensor: int) -> bool:

    tempo_atual = time.time()

    ultimo = ultimo_envio.get(id_sensor, 0)

    if tempo_atual - ultimo >= INTERVALO_MINIMO_DE_TEMPO:

        ultimo_envio[id_sensor] = tempo_atual
        return True

    return False


@app.post("/sensor")
async def receber_dados(data: SensorData):

    if not pode_enviar(data.id_sensor):

        raise HTTPException(
            status_code=429,
            detail="Intervalo mínimo não respeitado"
        )

    payload = {
        "api_key": THINGSPEAK_API_KEY,
        "field1": int(data.estado_do_alimentador),
    }

    async with httpx.AsyncClient() as client:

        resposta = await client.post(
            "https://api.thingspeak.com/update.json",
            data=payload
        )

    if resposta.status_code != 200:

        raise HTTPException(
            status_code=500,
            detail="Erro ao enviar ao ThingSpeak"
        )

    return {
        "status": "enviado",
        "thingspeak": resposta.text
    }

@app.get("/")
def home():
    return {"resposta": "ok"}