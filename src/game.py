 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 12:03:54 2022

@author: hasti
"""

import pygame
import os
import numpy as np
from logic import Logic

logic = Logic()
#%% constant variables

# dimensions of the game screen
WIDTH = 800   # pixels
HEIGHT = 800

# no. rows and columns of the chess board
ROWS = 8
COLS = 8

# size of each square
SQSIZE = WIDTH // ROWS

db_assets = "./chess_ai/assets/images/imgs-128px"
piece_id_dic = {-1:'black_pawn', -2:'black_rook', -3:'black_knight', -4:'black_bishop', -5:'black_queen', -6:'black_king',
                 1:'white_pawn', 2:'white_rook', 3:'white_knight', 4:'white_bishop', 5:'white_queen', 6:'white_king', 0:''}

#%%
class Game:
    """
    taking care of everything that needs to be drawn on the surface
    """
    
    def __init__(self):
        
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.is_debug = False
        # initial state of the board when the game starts
        self.init_np_board = self.f_init_np_board (stalemate = False, checkmate = True)
        # current state of the board after movement of a piece (, which in the beginning of the game is equal to initial state of the board)
        self.curr_np_board = self.init_np_board
        self.piece_id_dic = piece_id_dic
        
        # initialize the board with a certain configuration i.e. pieces and their locations, which is useful for debugging purposes
        # self.init_board(debug=True)
        
        
    #%%# init board function
    def f_init_np_board (self, stalemate = False, checkmate = False):
        
        """
        piece ids and their initial location on the chess board
        """
        np_board = np.zeros((8,8), dtype = 'int')
        
        if not stalemate and not checkmate :
            
            # -1: upper section of the board: black
            np_board [0,0] = -2 # left rook
            np_board [0,1] = -3 # left knight
            np_board [0,2] = -4 # left bishop
            np_board [0,3] = -5 # queen
            np_board [0,4] = -6 # king
            np_board [0,5] = -4 # right bishop
            np_board [0,6] = -3 # right knight
            np_board [0,7] = -2 # right rook
            # +1: lower section of the board: white
            np_board [7,0] = 2 # left rook
            np_board [7,1] = 3 # left knight
            np_board [7,2] = 4 # left bishop
            np_board [7,3] = 5 # queen
            np_board [7,4] = 6 # king
            np_board [7,5] = 4 # right bishop
            np_board [7,6] = 3 # right knight
            np_board [7,7] = 2 # right rook
            # pawn in lower and upper section
            for col in range(np_board.shape[1]): 
                np_board [1,col] = -1
                np_board [6,col] = 1 
        
        elif stalemate:

            # # stalemate scenario 1 (black king)
            # np_board [0,0] = -6 
            # np_board [2,1] = 6 
            # np_board [2,2] = 3 
            
            # # stalemate scenario 1 (white king)
            # np_board [0,0] = 6 
            # np_board [2,1] = -6 
            # np_board [2,2] = -3 
            
            # stalemate scenario 2 (black king)
            np_board [7,0] = -6 
            np_board [6,0] = -1 
            np_board [5,1] = 5 
            np_board [0,1] = 6
        
        elif checkmate:
            
            np_board [0,4] = -6 
            np_board [1,4] = -1 
            np_board [1,5] = -1 
            np_board [3,0] = 4 
            np_board [7,3] = 2
            np_board [7,6] = 6 
             
     
        return np_board
    
    #%% background
    
    def show_bg(self, surface): # surface: self.screen in Main class __init__
        """
        show chess background
        """
    
        # color of each square
        for row in range(ROWS): 
            for col in range(COLS):
                if (col + row) % 2 == 0:     # even col and row
                    color = (0, 255, 255)    # aqua
                elif (col + row) % 2 == 1:   # odd col and row
                    color = (0,191,255)      # deep blue sky
                
                # where on the screen and how large to draw the rectangular
                # rect = (hpos, vpos, length, width) # pos: starting from (0,0) at top left corner
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                
                # draw the square
                pygame.draw.rect(surface, color, rect)
    
    #%% rendering images
    
    def img_blit(self, color, piece, row, col, screen): # self.screen in Main class __init__
        
        """ draw each piece image on its corresponding square on the board (starting of the game)
        """
        
        self.width, self.height = int(WIDTH/8), int(HEIGHT/8)
        self.image_name = color + '_' + piece + '.png'
        self.image = pygame.image.load(os.path.join(db_assets,self.image_name))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        screen.blit(self.image, (col*SQSIZE, row*SQSIZE)) # index starts from 0 to 7 
        
    def render_pieces (self, screen):
        
        """ draw all pieces on their corresponding squares on the board (starting of the game)
        """

        init_np_board = self.init_np_board

        for row in range(init_np_board.shape[0]):
            for col in range(init_np_board.shape[1]):

                # 1: white (lower side of the board)    
                if init_np_board[row, col] == abs(init_np_board[row, col]):
                    color = 'white'
                    if init_np_board[row, col] == 1:
                        self.img_blit(color, 'pawn', row, col, screen)
                    elif init_np_board[row, col] == 2:
                        self.img_blit(color, 'rook', row, col, screen)
                    elif init_np_board[row, col] == 3:
                        self.img_blit(color, 'knight', row, col, screen)
                    elif init_np_board[row, col] == 4:
                        self.img_blit(color, 'bishop', row, col, screen)
                    elif init_np_board[row, col] == 5:
                        self.img_blit(color, 'queen', row, col, screen)
                    elif init_np_board[row, col] == 6:
                        self.img_blit(color, 'king', row, col, screen)
                
                # -1: black (upper part of the board)
                elif init_np_board[row, col] != abs(init_np_board[row, col]):
                    color = 'black'
                    if init_np_board[row, col] == -1:
                        self.img_blit(color, 'pawn', row, col, screen)
                    elif init_np_board[row, col] == -2:
                        self.img_blit(color, 'rook', row, col, screen)
                    elif init_np_board[row, col] == -3:
                        self.img_blit(color, 'knight', row, col, screen)
                    elif init_np_board[row, col] == -4:
                        self.img_blit(color, 'bishop', row, col, screen)
                    elif init_np_board[row, col] == -5:
                        self.img_blit(color, 'queen', row, col, screen)
                    elif init_np_board[row, col] == -6:
                        self.img_blit(color, 'king', row, col, screen)
                        
    #%% checking the validity of a move

    def draw_piece (self, moving_piece_id, move_from_row, move_from_col, move_to_row, move_to_col, screen):
        
        """ drawing a piece in the new loc and updatuing the state of the board i.e np_board
        """
 
        color = piece_id_dic[moving_piece_id][0:5] # e.g. 'balck pawn' -> black
        piece = piece_id_dic[moving_piece_id][6:]  # e.g. 'white pawn' -> pawn
        
        # draw the piece image in the destination loc
        self.img_blit(color, piece, move_to_row, move_to_col, screen) 
        # clear the piece image from the source location
        self.curr_np_board[move_from_row, move_from_col] = 0
        # update the state of the board after a piece has been moved
        self.curr_np_board[move_to_row, move_to_col] = moving_piece_id
   
#%% moving the piece

    # def draw_piece_in_move_mask_equal_to_one (self, curr_np_board, move_mask_piece, move_from_row, move_from_col, move_to_row, move_to_col, screen):
        
    #     if move_mask_piece [move_to_row, move_to_col] == 1:
    #         self.draw_piece (curr_np_board[move_from_row, move_from_col], move_from_row, move_from_col, move_to_row, move_to_col, screen)
    #         self.piece_is_moved = True

    def move_piece (self, curr_np_board, move_from_row, move_from_col, move_to_row, move_to_col, screen):
        
        piece_is_moved = False
        piece_id = curr_np_board[move_from_row, move_from_col]
        
        # p    
        if abs(piece_id) == 1:             
            move_mask_piece = logic.f_move_mask_p (curr_np_board, move_from_row, move_from_col)

        # r
        elif abs(piece_id) == 2: 
             move_mask_piece = logic.f_move_mask_r (curr_np_board, move_from_row, move_from_col)
               
        # k
        elif abs(piece_id) == 3: 
            move_mask_piece = logic.f_move_mask_k (curr_np_board, move_from_row, move_from_col)      
            
        # b
        elif abs(piece_id) == 4: 
            move_mask_piece = logic.f_move_mask_b (curr_np_board, move_from_row, move_from_col)
            
        # q
        elif abs(piece_id) == 5: 
            move_mask_piece = logic.f_move_mask_q (curr_np_board, move_from_row, move_from_col)
            
        # kk 
        elif abs(piece_id) == 6: 
            move_mask_piece = logic.f_move_mask_kk (curr_np_board, move_from_row, move_from_col)
        
        # self.draw_piece_in_move_mask_equal_to_one (curr_np_board, move_mask_piece, move_from_row, move_from_col, move_to_row, move_to_col, screen)
        if move_mask_piece [move_to_row, move_to_col] == 1:
            self.draw_piece (curr_np_board[move_from_row, move_from_col], move_from_row, move_from_col, move_to_row, move_to_col, screen)
            piece_is_moved = True
        
        return piece_is_moved
        

# if __name__ == '__main__':
    # game = Game()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
            
            
    
