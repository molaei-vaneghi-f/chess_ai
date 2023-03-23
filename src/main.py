
from game import Game
from logic import Logic
import os, sys
import pygame
import numpy as np


# Game class takes care of all that needs to be drawn on the screen
logic = Logic()
game = Game()
WIDTH = game.WIDTH
HEIGHT = game.HEIGHT
curr_np_board = game.curr_np_board
piece_id_dic = game.piece_id_dic
 
pygame.init()
screen = pygame.display.set_mode ((WIDTH, HEIGHT))
pygame.display.set_caption ('Playing Chess with My AI Buddy!')


#%% game loop

white_turn = True
black_turn = False

white_king_is_checked = False
black_king_is_checked = False


# def if_a_move_resolves_the_check (curr_np_board, color_of_king):
    
#     """ returns True if a move will save the king from the check condition! """

#     king_is_still_checked = True

#     # make an abstract board 
#     np_board = curr_np_board.copy() 
#     # update the state of the abstract board based on the user clicks and NOT actual movement of the pieces
#     np_board [move_to_row, move_to_col] = moving_piece_id
#     np_board [move_from_row, move_from_col] = 0
#     print(f'difference btw curr_np_board and np_board: \n rows: {np.where(curr_np_board != np_board)[0]} \n columns: {np.where(curr_np_board != np_board)[1]} ')
    
#     if color_of_king == 'white':
#         loc_king = np.where(np_board == 6)
#         color_of_mask = 'black'
#     elif color_of_king == 'black':
#         loc_king = np.where(np_board == -6)
#         color_of_mask = 'white'
        
#     # with the new state of curr_np_board i.e. after a piece is hypothetically moved, re-calculate the thread mask threating the king
#     mask_threating_the_king_actual = logic.f_threat_mask_allpieces (curr_np_board, color_of_mask)
#     mask_threating_the_king_hypoth = logic.f_threat_mask_allpieces (np_board, color_of_mask)
#     print(f'mask_threating_the_king actual vs hypoth: \n {np.where(mask_threating_the_king_actual != mask_threating_the_king_hypoth)}')
    
#     # did this hypothetical move of a piece, save the king? 
#     if mask_threating_the_king_hypoth [loc_king[0], loc_king[1]] == 0:
#         king_is_still_checked = False
        
#     # if not, it was an INVALID move, so dont do anything, do not actually move that  piece
#     elif mask_threating_the_king_hypoth [loc_king[0], loc_king[1]] == 1:
#         print('white king is still checked! make a move to resolve the check.')
    
#     return king_is_still_checked

#%% game loop

while True:
    
    game.show_bg(screen)
    # draw pieces on specific locations on the screen i.e. chess board
    game.render_pieces(screen)

    #%% event loop:
    
    for event in pygame.event.get():
        # print(event)
        # click = pygame.mouse.get_pressed()
        # mousex, mousey = pygame.mouse.get_pos()
        # print(click, mousex, mousey)
        
        if pygame.event == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # if the mouse is clicked (left, right, or misddle bottom)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # event.pos: (x,y) 0 < x < WIDTH (800 pixels), 0 < y < HEIGHT (800 pixels)
            # event.button: 1-> left-click, 2-> middle-click, 3-> right-click
            # print(f'In the current event loop, mouse (x,y) position: {event.pos}, clicked button: {event.button}')
            # row: event.pos[1]//100, col: event.pos[0]//100 
            # curr_np_board[row, col])

            #%% moving a piece (left-click: select the piece, right-click: put it at the position of right-click)
            
            # left-click
            if event.button == 1: 
                move_from_row = event.pos[1]//100 
                move_from_col = event.pos[0]//100
                moving_piece_id = curr_np_board[move_from_row, move_from_col]
                # print(f'moving_piece_name: {piece_id_dic[curr_np_board[event.pos[1]//100, event.pos[0]//100]]}')
                # print(f'moving_piece_id: {moving_piece_id}')
                # print(f'moving piece color: {piece_id_dic[moving_piece_id][0:5]}')     
            
            # right-click    
            elif event.button == 3: 
                
                move_to_row = event.pos[1]//100
                move_to_col = event.pos[0]//100
                
                # print(f'coordinates of the source loc: {(move_from_row,move_from_col)} *100 pixels \ncoordinates of the destination loc: {(move_to_row,move_to_col)} *100 pixels')
                
                #%% white
                
                if moving_piece_id > 0 and white_turn == True: 
                    
                    white_king_will_be_checked_after_this_move = \
                        logic.king_will_be_checked_after_this_move (curr_np_board, 'white', move_from_row, move_from_col, move_to_row, move_to_col)
                    
                    # before moving any piece, see if the king is checked or not
                    if not white_king_is_checked and not white_king_will_be_checked_after_this_move:
                        white_piece_is_moved = game.move_piece (curr_np_board, move_from_row, move_from_col, move_to_row, move_to_col, screen)
                        
                        # the following if condition should be repeated inside both parent if conditions i.e. 
                        # if not white_king_is_checked: and elif white_king_is_checked:/if not king_is_still_checked:
                        # if you put it outside the above two parent conditions the state of "white_piece_is_moved" variable 
                        # will spill over to the current event from the previous event REGARDLESS of whether or not a white piece was ACTUALLY moved i.e.
                        # it will remember the state of this variablle from the last movement of a white piece. Same holds true for the black.
                        
                        # only after a valid click, which leads to a valid move, the turns are reversed 
                        if white_piece_is_moved:
                            white_turn = False
                            black_turn = True
                            
                    elif white_king_is_checked:
                        # white_king_is_still_checked = if_a_move_resolves_the_check (curr_np_board, 'white')
                        white_king_is_still_checked = \
                            logic.king_will_still_be_checked_after_this_move (curr_np_board, 'white', move_from_row, move_from_col, move_to_row, move_to_col)
                        
                        if not white_king_is_still_checked and not white_king_will_be_checked_after_this_move:
                            white_piece_is_moved = game.move_piece (curr_np_board, move_from_row, move_from_col, move_to_row, move_to_col, screen)

                            if white_piece_is_moved:
                                white_turn = False
                                black_turn = True
                    
                    
                #%% black
                
                elif moving_piece_id < 0 and black_turn == True:
                    
                    black_king_will_be_checked_after_this_move = \
                        logic.king_will_be_checked_after_this_move (curr_np_board, 'black', move_from_row, move_from_col, move_to_row, move_to_col)
                    
                    if not black_king_is_checked and not black_king_will_be_checked_after_this_move:
                        black_piece_is_moved = game.move_piece (curr_np_board, move_from_row, move_from_col, move_to_row, move_to_col, screen)
                        
                        if black_piece_is_moved:
                            white_turn = True
                            black_turn = False
                            
                    elif black_king_is_checked:
                        # black_king_is_still_checked = if_a_move_resolves_the_check (curr_np_board, 'black')
                        black_king_is_still_checked = \
                            logic.king_will_still_be_checked_after_this_move (curr_np_board, 'black', move_from_row, move_from_col, move_to_row, move_to_col)
                        
                        if not black_king_is_still_checked and not black_king_will_be_checked_after_this_move:
                            black_piece_is_moved = game.move_piece (curr_np_board, move_from_row, move_from_col, move_to_row, move_to_col, screen)
        
                            if black_piece_is_moved:
                                white_turn = True
                                black_turn = False
                                                    

                #%% before the player makes a move, inform him if his king is checked
                
                if white_turn:
                    
                    white_king_is_checked = logic.f_king_is_checked (curr_np_board, 'white')
                    if white_king_is_checked:
                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \n white king is checked!')
                        
                    stalemate_white = logic.f_stalemate (curr_np_board, 'white')
                    if stalemate_white:
                        print(' >>>>>>>>>>>>>> STALEMATE FOR WHITE <<<<<<<<<<<<<<')
                        
                    checkmate_white = logic.f_checkmate  (curr_np_board, 'white')
                    if checkmate_white:
                        print(' >>>>>>>>>>>>>> CHECKMATE FOR WHITE <<<<<<<<<<<<<<')
                
                elif black_turn:
                    
                    black_king_is_checked = logic.f_king_is_checked (curr_np_board, 'black')
                    if black_king_is_checked:
                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \n black king is checked!')
                    
                    stalemate_black = logic.f_stalemate (curr_np_board, 'black') 
                    if stalemate_black:
                        print(' >>>>>>>>>>>>>> STALEMATE FOR BLACK <<<<<<<<<<<<<<')
                    
                    checkmate_black = logic.f_checkmate  (curr_np_board, 'black')
                    if checkmate_black:
                        print(' >>>>>>>>>>>>>> CHECKMATE FOR BLACK <<<<<<<<<<<<<<')

                # after one right-click (following the previous left-click), further right-clicks should not result in a piece being moved
                moving_piece_id = 0                    
                
                
                
    # last line inside the game loop: update the display/screen with what we have drawn
    # tip: .flip() updates the contents of the entire display => slower
    # tip: .update() updates a portion of the screen instead of the entire area of the screen when given an input argument => faster
        # without input args, updates the entire disply
    # pygame.display.flip()
    pygame.display.update() 
    
    
