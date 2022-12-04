import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends_list = get_friends(user_id=user_id, fields=["bdate"])
    dates = list()
    for friend in friends_list.items:
        try:
            date = str(friend.get('bdate'))  # type : ignore
            if date.count(".") == 2:
                dates.append(int(date[date.rfind(".") + 1 :]))
        except KeyError:
            pass
    return sum(dates) // len(dates)
