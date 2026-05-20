from pydantic import BaseModel

class SensorData(BaseModel):
    id_sensor: int
    estado_do_alimentador: bool