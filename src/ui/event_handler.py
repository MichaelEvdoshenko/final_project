import pygame
from typing import Any, Dict, Optional, Tuple


class EventHandler:
    def __init__(self) -> None:
        pass

    def handle_start_screen_events(self,
                                   event: pygame.event.Event,
                                   screen_elements: Dict[str, Any],
                                   mouse_pos: Tuple[int,
                                                    int]) -> Optional[str]:
        r = None

        screen_elements['vs_friend_btn'].check_hover(mouse_pos)
        screen_elements['vs_bot_btn'].check_hover(mouse_pos)
        screen_elements['back_btn'].check_hover(mouse_pos)

        screen_elements['mcts_rb'].check_hover(mouse_pos)
        screen_elements['qlearning_rb'].check_hover(mouse_pos)

        for t in screen_elements['size_buttons']:
            t[0].check_hover(mouse_pos)

        screen_elements['player_first_rb'].check_hover(mouse_pos)
        screen_elements['bot_first_rb'].check_hover(mouse_pos)

        if screen_elements['vs_friend_btn'].is_clicked(mouse_pos, event):
            r = "friend"
        else:
            if screen_elements['vs_bot_btn'].is_clicked(mouse_pos, event):
                r = "bot"
            else:
                if screen_elements['back_btn'].is_clicked(mouse_pos, event):
                    r = "exit"

        if screen_elements['mcts_rb'].check_click(mouse_pos, event):
            screen_elements['bot_choice'] = screen_elements['mcts_rb'].value
        else:
            if screen_elements['qlearning_rb'].check_click(mouse_pos, event):
                rd = screen_elements['qlearning_rb']
                screen_elements['bot_choice'] = rd.value

        for t in screen_elements['size_buttons']:
            if t[0].check_click(mouse_pos, event):
                screen_elements['size'] = t[0].value

        if screen_elements['player_first_rb'].check_click(mouse_pos, event):
            sup = screen_elements['player_first_rb']
            screen_elements['first_turn'] = sup.value
        else:
            if screen_elements['bot_first_rb'].check_click(mouse_pos, event):
                rb = screen_elements['bot_first_rb']
                screen_elements['first_turn'] = rb.value

        return r

    def handle_game_events(self,
                           event: pygame.event.Event,
                           gameinter: Any,
                           mouse_pos: Tuple[int, int]) -> Optional[str]:
        r = None

        gameinter.back_btn.check_hover(mouse_pos)
        gameinter.restart_btn.check_hover(mouse_pos)

        if gameinter.back_btn.is_clicked(mouse_pos, event):
            r = "back"
        else:
            if gameinter.restart_btn.is_clicked(mouse_pos, event):
                gameinter.restart_game()
                return None

        ended = gameinter.game.winner is not None

        if gameinter.game_mode == "bot":
            if gameinter.current_player == gameinter.bot_player:
                return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not ended:
                    c = gameinter.get_cell_at_pos(mouse_pos)
                    if c:
                        if gameinter.game.field[c[0]][c[1]] == ' ':
                            gameinter.make_move(c[0], c[1],
                                                gameinter.current_player)
                            r = "move_made"
        return r
