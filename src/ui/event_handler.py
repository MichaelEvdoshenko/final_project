import pygame

class EventHandler:
    def __init__(self):
        pass
    
    def handle_start_screen_events(self, event, screen_elements, mouse_pos):
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
                screen_elements['bot_choice'] = screen_elements['qlearning_rb'].value
            
        for t in screen_elements['size_buttons']:
            if t[0].check_click(mouse_pos, event):
                screen_elements['size'] = t[0].value
                
        if screen_elements['player_first_rb'].check_click(mouse_pos, event):
            screen_elements['first_turn'] = screen_elements['player_first_rb'].value
        else:
            if screen_elements['bot_first_rb'].check_click(mouse_pos, event):
                screen_elements['first_turn'] = screen_elements['bot_first_rb'].value
            
        return r
    
    def handle_game_events(self, event, game_interface, mouse_pos):
        r = None
    
        game_interface.back_btn.check_hover(mouse_pos)
        game_interface.restart_btn.check_hover(mouse_pos)
    
        if game_interface.back_btn.is_clicked(mouse_pos, event):
            r = "back"
        else:
            if game_interface.restart_btn.is_clicked(mouse_pos, event):
                game_interface.restart_game()
                return None

        ended = game_interface.game.winner is not None
        
        if game_interface.game_mode == "bot":
            if game_interface.current_player == game_interface.bot_player:
                return None
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not ended:
                    c = game_interface.get_cell_at_pos(mouse_pos)
                    if c:
                        if game_interface.game.field[c[0]][c[1]] == ' ':
                            game_interface.make_move(c[0], c[1], game_interface.current_player)
                            r = "move_made"
                    
        return r