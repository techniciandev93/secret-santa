from telegram_bot.models import Gamer


def generator_separated_users(users):
    while True:
        for user in users:
            yield user


def get_user(gen_user, user, separated_users):
    while True:
        next_user = next(gen_user)
        if next_user != user and next_user not in separated_users.values():
            return next_user


def main_separated(users):
    if len(users) < 3:
        raise ValueError('Мало участников для жеребьевки')

    separated_users = dict.fromkeys(users, None)
    user_generator = generator_separated_users(separated_users)
    
    for user in separated_users:
        separated_users[user] = get_user(user_generator, user, separated_users)
    
    return separated_users
