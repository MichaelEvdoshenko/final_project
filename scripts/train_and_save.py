from src.ai.bot_Q_learning import Q_learning_bot
from src.core.game import Krestik_nolik
import json
import os


def train_and_save_to_json(size=3, first_turn="bot"):

    game = Krestik_nolik(size=size)
    bot = Q_learning_bot(game=game, alfa=0.2, eps=0.9)

    bot.learn(first_turn)
    q_table_for_json = {}
    for state_hash, q_values in bot.massive_Q.items():
        q_table_for_json[state_hash] = q_values.tolist()

    filename = f"models/q_table_{size}x{size}_{first_turn}.json"
    os.makedirs("models", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(q_table_for_json, f, indent=2, ensure_ascii=False)

    return bot


if __name__ == "__main__":
    configs = [
        (3, "bot"),
        (3, "player"),
        (4, "bot"),
        (4, "player"),
        (5, "bot"),
        (5, "player"),
    ]

    for size, first_turn in configs:
        train_and_save_to_json(size, first_turn)
