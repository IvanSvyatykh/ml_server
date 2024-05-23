import json
import torch

from ollama import AsyncClient


from speechkit import model_repository
import speechkit


from speechkit.stt import AudioProcessingType
from fastapi import APIRouter, UploadFile, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/classify", tags=["classification"])


DEFAULT_SYSTEM_PROMPT_TYPE = (
    "Ты работник организации,который классифицирует ответ пользователя на категории: AЗС, Яма, ДТП, Закон, Кафе, СТО, Развлечения, Парковка, Здоровье, Общее."
    "АЗС - Автомобильная заправочная станция — комплекс оборудования на придорожной территории, предназначенный для заправки топливом транспортных средств, на ней водитель сможет заправиться бензином, дизелем, газом."
    "Яма - Вырытое или образовавшееся углубление в земле."
    "ДТП - Дорожно-транспортное происшествие — событие, возникшее в процессе движения по дороге транспортного средства и с его участием, при котором погибли или пострадали люди или повреждены транспортные средства, сооружения, грузы, либо причинён иной материальный ущерб."
    "Закон - водитель заметил, как кто-то нарушает закон и хочет сообщить об этом. В данную категорию попадают: ограбления, воровство, нападение, угрозы."
    "Кафе - это место, где человек сможет купить еды или остановиться, для того чтобы поесть."
    "СТО - это место, где человек сможет произвести обслуживание своего транспорта или его починку."
    "Развлечение - это места, где человек сможет отдохнуть или провести время, это может быть: озера, фестивали, курорты, базы отдыха."
    "Парковка - это места, где человек сможет безопасно припарковать автомобиль или оставить его на длительное время."
    "Здоровье - это категория, говорит о том, что жизни или здоровью человека, что-то угрожает, это может быть стихийное бедствие, проблемы со здровьем."
    "Общее - Не смог определить категорию и отнести к конкретной"
    "Ты должен дать ответ к какой категории относиться данный вопрос. Ответ должен принадлежать одной из категорий  описанных выше, другие варианты использовать запрещенно. Длина ответа должна быть одним словом."
    "Вопрос пользователя: "
)


@router.on_event("startup")
def load_model() -> None:
    """Загружает модели при fneuifbeuinстарте сервера. Исполняется один раз."""
    speechkit.configure_credentials(
        yandex_credentials=speechkit.creds.YandexCredentials(
            api_key="AQVN2l4qzMgPkk2UX-d9ZaZuKcN75N9OaUubwnoR"
        )
    )


@router.post("/audio/road")
async def answer_on_audio(file: UploadFile):
    model = model_repository.recognition_model()
    model.model = "general"
    model.language = "ru-RU"
    model.audio_processing_type = AudioProcessingType.Full

    result = model.transcribe(await file.read())
    question = str(result[0])
    message = {
        "role": "user",
        "content": DEFAULT_SYSTEM_PROMPT_TYPE + question,
    }
    response = await AsyncClient().chat(model="llama3", messages=[message])

    return JSONResponse(json.dumps({"label": response["message"]["content"]}))


@router.post("/text/road/{question}")
async def answer_on_text(question):
    """Эндпоинт для ответа на сообщение.

    question: Сообщение на которое нужно ответить.
    """
    message = {
        "role": "user",
        "content": DEFAULT_SYSTEM_PROMPT_TYPE + question,
    }
    response = await AsyncClient().chat(model="llama3", messages=[message])

    return JSONResponse(json.dumps({"label": response["message"]["content"]}))
