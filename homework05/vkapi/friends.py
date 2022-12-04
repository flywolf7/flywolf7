import dataclasses
import math
import time
import typing as tp

from vkapi import Session
from vkapi.config import VK_CONFIG

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    s = Session(str(VK_CONFIG["domain"]))
    friends_json = s.get(
        "friends.get",
        access_token=VK_CONFIG["access_token"],
        user_id=user_id,
        count=count,
        offset=offset,
        fields=fields,
        v=VK_CONFIG["version"],
    ).json()

    to_return = FriendsResponse(
        friends_json["response"]["count"], friends_json["response"]["items"]
    )
    return to_return


def get_friends_list(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
):
    s = Session(str(VK_CONFIG["domain"]))
    friends_json = s.get(
        "friends.get",
        access_token=VK_CONFIG["access_token"],
        user_id=user_id,
        count=count,
        offset=offset,
        fields=fields,
        v=VK_CONFIG["version"],
    ).json()

    return friends_json["response"]["items"]


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Список идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """

    if target_uids is not None and len(target_uids) > 100:
        itr = math.ceil(len(target_uids) / 100)
    else:
        itr = 1

    s = Session(str(VK_CONFIG["domain"]))
    mutual = list()
    for i in range(itr):
        response = s.get(
            "friends.getMutual",
            access_token=VK_CONFIG["access_token"],
            source_uid=source_uid,
            target_uid=target_uid,
            target_uids=target_uids,
            order=order,
            count=100,
            offset=100 * i,
            v=VK_CONFIG["version"],
        ).json()["response"]
        mutual += response

        if i % 3 == 0:
            time.sleep(1)

    return mutual
