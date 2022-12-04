import math
import time
import typing as tp

import pandas as pd
import requests
from pandas import json_normalize
from vkapi.config import VK_CONFIG


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    if domain == "":
        code = f"""return API.wall.get(&
                    "owner_id": "{owner_id}",
                    "offset": {offset},
                    "count": {count},
                    "filter": "{filter}",
                    "extended": {extended},
                    "v": "5.131",
                    *);"""
    else:
        code = f"""return API.wall.get(&
                            "owner_id": "{owner_id}",
                            "domain": "{domain}",
                            "offset": {offset},
                            "count": {count},
                            "filter": "{filter}",
                            "extended": {extended},
                            "v": "5.131",
                            *);"""
    code = code.replace("&", "{").replace("*", "}")

    response_json = requests.post(
        "https://api.vk.com/method/execute",
        data={
            "access_token": VK_CONFIG["access_token"],
            "code": code,
            "v": VK_CONFIG["version"],
        },
    ).json()

    return response_json["response"]["items"]


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.
    @see: https://vk.com/dev/wall.get
    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """

    to_return: list = []
    for i in range(math.ceil(count / 2500)):
        response = get_posts_2500(
            owner_id, domain, i * 2500, max_count, max_count, filter, extended, fields
        )
        to_return += response
        time.sleep(1)
    return json_normalize(to_return)
