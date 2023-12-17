import random
import asyncio
from .models import Game, Patricipants, Givers
from asgiref.sync import sync_to_async

from secret_santa.bot_logic.loader import bot


def get_participants(game):
    players = []
    for player in Patricipants.objects.select_related('game').filter(game=game):
        players.append(player)
    return players

def perform_pairing(games):
    for game in games:
        # начало разибиения на пары
        participants = get_participants(game)

        shift = random.randint(1, len(participants) - 1)
        pairs = {}
        gifters_arr = []
        for count, player in enumerate(participants):
            pairs[player] = participants[(count + shift) % len(participants)]
            message = f"Твой партнер - {pairs[player].name}, " \
                      f"интересуется {pairs[player].interests}, " \
                      f"хочет сказать тебе следующее\n{pairs[player].letter_to_santa}"
            gifters = Givers(
                game=game,
                givers=player,
                recipient=pairs[player],
                message=message,
            )
            gifters_arr.append(gifters)
            gifters.save()
        return gifters_arr


