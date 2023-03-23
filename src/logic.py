
import numpy as np

class Logic:
    """
    taking care of making and evaluating the logic of the game
        - auxiliary functions (have nothing to do with the current state of the board or 
                               receive the current state of the board, but do not change it)
    """
    
    def __init__(self):
        
        self.is_debug = False
        
    #%% general auxiliary functions

    def destination_is_occupied (self, curr_np_board, dest_pos):
        
        """ checks if there is a piece in the destination 
        """
        dest_row, dest_col = dest_pos
        
        if 0 <= dest_row <= 7 and 0 <= dest_col <= 7:
            if curr_np_board[dest_row, dest_col] != 0:
                return True
            else:
                return False
            
        
    def destination_piece_is_friend (self, curr_np_board, sour_pos, dest_pos):
        
        """ checks if the piece in the destination loc has the same color as the piece in the source loc i.e. is a friend
        """
        
        sour_row, sour_col = sour_pos
        dest_row, dest_col = dest_pos
        
        # make sure the destination is occupied before checking if it is a friend or not
        # if destination is NOT occupied, throw an error and STOP execution of the script altogether
        assert curr_np_board[dest_row, dest_col] != 0, 'Error: You are trying to see if the piece in the destination is a friend or not, but there is no piece in the destination!'
        
        if [dest_row, dest_col] != 0:
            if 0 <= dest_row <= 7 and 0 <= dest_col <= 7: 
                if curr_np_board[sour_row, sour_col] * curr_np_board[dest_row, dest_col] > 0:
                    return True
                else:
                    return False
                
                
    #%% pawn auxiliary functions

    def pawn_move_straight (self, curr_np_board, row, col, a, b, c, x1, x2):
        
        """ checks for valid locs to move the pawn along the straight line forward and adds them to the pawn mask
        """
        mask = np.zeros(curr_np_board.shape, dtype = curr_np_board.dtype)
   
        if row == a:
            if not self.destination_is_occupied (curr_np_board, (x1, col)):
                mask[x1, col] = 1
            if not self.destination_is_occupied (curr_np_board, (x2, col)):
                mask[x2, col] = 1
        elif b <= row < c:
            if not self.destination_is_occupied (curr_np_board, (x1, col)):
                mask[x1, col] = 1
                
        return mask
                
    
    def pawn_attack_diagonal (self, curr_np_board, x1, y1, y2):
        
        """ checks for valid locs to move the pawn along the diagonal line forward i.e. valid attack locs for the pawn and adds them to the pawn mask
        """
        mask = np.zeros(curr_np_board.shape, dtype = curr_np_board.dtype)
        
        if self.destination_is_occupied (curr_np_board, (x1, y1)) and 0 <= y1 < 8:
            mask[x1, y1] = 1 
        if self.destination_is_occupied (curr_np_board, (x1, y2)) and 0 <= y2 < 8:  
            mask[x1, y2] = 1 
    
        return mask
                
            
    def check_cond_pawn (self, curr_np_board, row, col):
        
        """ checks for pawn valid locations either along the straight line or diagonally (attacking) and adds them to the pawn mask
        
            return a list of arrays with 3 elements:
                - first element: an array representing the move_mask_p_move_straight
                - second element: an array representing the move_mask_p_attack_diagonal
                - third element: an array representing the move_mask_p_move_straight_attack_diagonal
        
        """
        
        # move_mask_p = []
        
        if curr_np_board[row, col] == -1:   # bp, moving down
            a = 1
            b = 2
            c = curr_np_board.shape[1] - 1  # 7 
            x1 = row+1
            x2 = row+2
            y1 = col-1
            y2 = col+1
    
        elif curr_np_board[row, col] == 1:  # wp, moving up
            a = 6
            b = 1
            c = curr_np_board.shape[1] - 2  # 6
            x1 = row-1
            x2 = row-2
            y1 = col-1
            y2 = col+1

        move_mask_p_move_straight = self.pawn_move_straight (curr_np_board, row, col, a, b, c, x1, x2)
        move_mask_p_attack_diagonal = self.pawn_attack_diagonal (curr_np_board, x1, y1, y2)
        move_mask_p_move_straight_attack_diagonal = move_mask_p_move_straight + move_mask_p_attack_diagonal
        # move_mask_p = move_mask_p [move_mask_p <=1] # this will flatten the array
        # move_mask_p [move_mask_p <=1]
        move_mask_p_move_straight_attack_diagonal [move_mask_p_move_straight_attack_diagonal > 1] = 1
        
        # move_mask_p [0] = move_mask_p_move_straight
        # move_mask_p [1] = move_mask_p_attack_diagonal
        # move_mask_p [2] = move_mask_p_move_straight_attack_diagonal
        move_mask_p = [move_mask_p_move_straight, move_mask_p_attack_diagonal, move_mask_p_move_straight_attack_diagonal]
        
        return move_mask_p
        
    #%% rook auxiliary functions
    
    def check_cond_rook_row (self, curr_np_board, sour_pos, range_row_idx):
        
        """ checks, in an incremental way (starting from the source loc), the horizontal line passing through the rook for all the valid locations
        """
        sour_row, sour_col = sour_pos
        mask = np.zeros(curr_np_board.shape, dtype = curr_np_board.dtype)
        
        for idx in range_row_idx:
            if self.destination_is_occupied (curr_np_board, (idx, sour_col)) and self.destination_piece_is_friend (curr_np_board, sour_pos, (idx, sour_col)):
            # if self.destination_piece_is_friend (curr_np_board, sour_pos, (idx, sour_col)):
                break
            if self.destination_is_occupied (curr_np_board, (idx, sour_col)) and not self.destination_piece_is_friend (curr_np_board, sour_pos, (idx, sour_col)):
            # if not self.destination_piece_is_friend (curr_np_board, sour_pos, (idx, sour_col)):
                mask[idx, sour_col] = 1
                break
            mask[idx, sour_col] = 1
            
        return mask
   
            
    def check_cond_rook_col (self, curr_np_board, sour_pos, range_col_idx): 
        
        """ checks, in an incremental way (starting from the source loc), the vertical line passing through the rook for all the valid locations
        """
        sour_row, sour_col = sour_pos
        mask = np.zeros(curr_np_board.shape, dtype = curr_np_board.dtype)
            
        for idx in range_col_idx:
            if self.destination_is_occupied (curr_np_board, (sour_row, idx)) and self.destination_piece_is_friend (curr_np_board, sour_pos, (sour_row, idx)):
            # if self.destination_piece_is_friend (curr_np_board, sour_pos, (sour_row, idx)):
                break
            if self.destination_is_occupied (curr_np_board, (sour_row, idx)) and not self.destination_piece_is_friend (curr_np_board, sour_pos, (sour_row, idx)):
            # if not self.destination_piece_is_friend (curr_np_board, sour_pos, (sour_row, idx)):
                mask[sour_row, idx] = 1
                break
            mask[sour_row, idx] = 1
            
        return mask

    #%% knight auxiliary functions
                        
    def check_cond_knight (self, curr_np_board, sour_pos):
        
        """ checks if any of all the possible 8 locations for the knight is valid, in which case it will be added to the mask
        """
        row, col = sour_pos
        mask = np.zeros(curr_np_board.shape, dtype = curr_np_board.dtype)
        
        k_all_8_poss_locs = [(row-2,col-1),(row-2,col+1),(row-1,col-2),(row-1,col+2),
                             (row+2,col-1),(row+2,col+1),(row+1,col-2),(row+1,col+2)]
        # if self.is_debug:
        #     print(f'source loc of the knight: {sour_pos} \n k_all_8_poss_locs: {k_all_8_poss_locs}')
        
        # loc_idx is a tuple, loc_idx[0]:row, loc_idx[1]:col
        for loc_idx in k_all_8_poss_locs:
            if 0 <= loc_idx[0] < 8 and 0 <= loc_idx[1] < 8:

                if self.destination_is_occupied (curr_np_board, loc_idx) and not self.destination_piece_is_friend (curr_np_board, sour_pos, loc_idx): 
                # if not self.destination_piece_is_friend (curr_np_board, sour_pos, loc_idx): 
                    mask[loc_idx[0], loc_idx[1]] = 1
                    # if self.is_debug:
                    #     print(f'destination {loc_idx} is occupied but NOT by a friend.')
  
                elif not self.destination_is_occupied (curr_np_board, loc_idx):
                    mask[loc_idx[0], loc_idx[1]] = 1  
                    # if self.is_debug:
                    #     print(f'destination {loc_idx} is NOT occupied.') 
        return mask
                        
    #%% pawn: building the move mask for EACH pieces: 
       
    def f_move_mask_p (self, curr_np_board, row, col):
        
        # checks for pawn valid locations along the straight line or diagonally (attacking) and adds them to the pawn mask
        move_mask_p3 = self.check_cond_pawn (curr_np_board, row, col)
        move_mask_p = move_mask_p3[2] # the third element of the list is both straight_line and attack_diagonal mask
        
        if self.is_debug:
            print(f'f_move_mask_p returns: \n {move_mask_p}')
            
        return move_mask_p
     
    #%% rook: building the move mask for EACH pieces:
    
    def f_move_mask_r (self, curr_np_board, row, col):

        # 1: left wing: [row, 0:col]
        move_mask_r_col1 = self.check_cond_rook_col (curr_np_board, (row, col), range(col-1,-1,-1))
        # 2: right wing: [row, col+1:]
        move_mask_r_col2 = self.check_cond_rook_col (curr_np_board, (row, col), range(col+1,8))       
        # 3: upper wing: [0:row, col]
        move_mask_r_row1 = self.check_cond_rook_row (curr_np_board, (row, col), range(row-1,-1,-1))
        # 4: lower wing: [row+1:8, col]
        move_mask_r_row2 = self.check_cond_rook_row (curr_np_board, (row, col), range(row+1,8))
        
        move_mask_r = move_mask_r_col1 + move_mask_r_col2 + move_mask_r_row1 + move_mask_r_row2
        # move_mask_r = move_mask_r [move_mask_r <=1] # this will flatten the array
        # move_mask_r [move_mask_r <= 1]
        # set elements with values higher than 1, to 1
        move_mask_r [move_mask_r > 1] = 1 
        
        if self.is_debug:
            print(f'f_move_mask_r returns: \n {move_mask_r}')
    
        return move_mask_r  
          
    #%% knigh: building the move mask for EACH pieces:

    def f_move_mask_k (self, curr_np_board, row, col):

        move_mask_k = self.check_cond_knight (curr_np_board, (row, col))
        
        if self.is_debug:
            print(f'f_move_mask_k returns: \n {move_mask_k}')
             
        return move_mask_k 
    
    #%% bishop: building the move mask for EACH pieces:
    
    def f_move_mask_b (self, curr_np_board, row, col):
        
        move_mask_b = np.zeros(curr_np_board.shape, dtype = curr_np_board.dtype)
        step_range = range(1,7) # this is an arbitrary range
        wing_list = ['top-left','top-right','bottom-left','bottom-right']
                
        for wing in wing_list: 
            for step in step_range:
            
                if wing == 'top-left':
                    row_idx = row-step
                    col_idx = col-step
                elif wing == 'top-right':
                    row_idx = row-step
                    col_idx = col+step
                elif wing == 'bottom-left':
                    row_idx = row+step
                    col_idx = col-step
                elif wing == 'bottom-right':
                    row_idx = row+step
                    col_idx = col+step   
                
               
                if 0 <= row_idx < 8 and 0 <= col_idx < 8:
                    if self.destination_is_occupied (curr_np_board, (row_idx, col_idx)) and not self.destination_piece_is_friend (curr_np_board, (row, col), (row_idx, col_idx)):
                        move_mask_b[row_idx, col_idx] = 1
                        break
                    if self.destination_is_occupied (curr_np_board, (row_idx, col_idx)) and self.destination_piece_is_friend (curr_np_board, (row, col), (row_idx, col_idx)):
                        break
                    if not self.destination_is_occupied (curr_np_board, (row_idx, col_idx)):
                        move_mask_b[row_idx, col_idx] = 1  
                        
        if self.is_debug:
            print(f'f_move_mask_b returns: \n {move_mask_b}')
            
        return move_mask_b
       
    #%% queen: building the move mask for EACH pieces:
        
    def f_move_mask_q (self, curr_np_board, row, col):
        
        move_mask_q = np.zeros(curr_np_board.shape, dtype = curr_np_board.dtype)
        move_mask_q = self.f_move_mask_r (curr_np_board, row, col) + self.f_move_mask_b (curr_np_board, row, col)
        move_mask_q [move_mask_q <= 1]
        
        if self.is_debug:
            print(f'f_move_mask_q returns: \n {move_mask_q}')
   
        return move_mask_q
    
    #%% king: building the move mask for EACH pieces:
        
    def f_move_mask_kk (self, curr_np_board, row, col, include_the_king_in_mask_calc = False):
        
        move_mask_kk = np.zeros(curr_np_board.shape, dtype = curr_np_board.dtype)

        if include_the_king_in_mask_calc == False:
            # black king can only be threatened by white pieces
            if curr_np_board[row, col] == -6:
                threat_mask_allpieces = self.f_threat_mask_allpieces (curr_np_board, 'white')
            # white king can only be threatened by black pieces
            elif curr_np_board[row, col] == 6:
                threat_mask_allpieces = self.f_threat_mask_allpieces (curr_np_board, 'black')
        
        elif include_the_king_in_mask_calc == True:
            threat_mask_allpieces = np.zeros(curr_np_board.shape, dtype=curr_np_board.dtype)
                   
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if 0 <= r < 8 and 0 <= c < 8:
                    
                    # dest loc should NOT be threatened by any other piece (OF THE OPPOSITE COLOR) in order for the king to move there (if its empty) or to kill the piece (OF THE OPPOSITE COLOR) located there.
                    if threat_mask_allpieces[r, c] == 0:
                        
                        if self.destination_is_occupied (curr_np_board, (r, c)) and not self.destination_piece_is_friend (curr_np_board, (row, col), (r, c)):
                            move_mask_kk[r, c] = 1
                            
                        elif not self.destination_is_occupied (curr_np_board, (r, c)):
                            move_mask_kk[r, c] = 1  
                 
        if self.is_debug:
            print(f'f_move_mask_kk returns: \n {move_mask_kk}')
            
        return move_mask_kk
    
        
    #%% building the threat/move mask for ALL pieces:    
                
    def f_threat_mask_allpieces (self, curr_np_board, color):
        
        """
        a mask that combines, for all pieces OF THE SAME COLOR, all the squares, to which they can be moved i.e. make a threat for pieces of the opposite color
        """
        
        if color == 'black':
            piece_id_list = list(range(-6, 0))
            piece_id_list.reverse()           # [-1, -2, -3, -4, -5, -6]
        elif color == 'white':
            piece_id_list = list(range(1, 7)) # [1, 2, 3, 4, 5, 6]
        
        threat_mask_allpieces = np.zeros(curr_np_board.shape, dtype=curr_np_board.dtype)
        
        for row in range(0, curr_np_board.shape[0]):
            for col in range(0, curr_np_board.shape[1]):
    
                # pawn
                if curr_np_board[row, col] == piece_id_list[0]:
                    # threat_mask_allpieces += self.f_move_mask_p (curr_np_board, row, col)   

                    # a list of arrays: first element: mask of moving straight, second: mask of attacking diagonally, third: both
                    move_mask_p3 = self.check_cond_pawn (curr_np_board, row, col)
                    # only attacking diagonally (2nd element) is the threating move of a pawn and not moving straight
                    move_mask_p_attack_diagonal = move_mask_p3[1]
                    threat_mask_allpieces += move_mask_p_attack_diagonal     
                            
                # rook
                elif curr_np_board[row,col] == piece_id_list[1]:                
                    threat_mask_allpieces += self.f_move_mask_r (curr_np_board, row, col)      
                # knight
                elif curr_np_board[row,col] == piece_id_list[2]:                
                    threat_mask_allpieces += self.f_move_mask_k (curr_np_board, row, col) 
                # bishop
                elif curr_np_board[row,col] == piece_id_list[3]:                
                    threat_mask_allpieces += self.f_move_mask_b (curr_np_board, row, col)
                # queen
                elif curr_np_board[row,col] == piece_id_list[4]: 
                    threat_mask_allpieces += self.f_move_mask_q (curr_np_board, row, col)
                # king 
                elif curr_np_board[row,col] == piece_id_list[5]:              
                    threat_mask_allpieces += self.f_move_mask_kk (curr_np_board, row, col, include_the_king_in_mask_calc = True) 
                    
        # set elements with values higher than 1, to 1
        threat_mask_allpieces [threat_mask_allpieces > 1] = 1 
                                             
        return threat_mask_allpieces 
    
    
    #%%
    def calc_hypoth_mask (self, curr_np_board, color_of_king, move_from_row, move_from_col, move_to_row, move_to_col):
        
        """ calculates a hypothetical mask based on the user click and NOT actual movement of a piece.
            this mask will be used to permit an ACTUAL movement of a piece later on only if that movement 
            either saves the king from the check condition (comes from enemy move) or does NOT result in king being checked (comes from friend) move!
        """
 
        moving_piece_id = curr_np_board[move_from_row, move_from_col]
        
        # make an abstract board 
        np_board = curr_np_board.copy() 

            
        # update the state of the abstract board based on the user clicks and NOT actual movement of the pieces
        np_board [move_to_row, move_to_col] = moving_piece_id
        np_board [move_from_row, move_from_col] = 0
        print(f'difference btw curr_np_board and np_board: \n rows: {np.where(curr_np_board != np_board)[0]} \n columns: {np.where(curr_np_board != np_board)[1]} ')
        
        if color_of_king == 'white':
            loc_king = np.where(np_board == 6)
            color_of_mask = 'black'
        elif color_of_king == 'black':
            loc_king = np.where(np_board == -6)
            color_of_mask = 'white'
            
        # with the new state of curr_np_board i.e. after a piece is hypothetically moved, re-calculate the thread mask threating the king
        mask_threating_the_king_actual = self.f_threat_mask_allpieces (curr_np_board, color_of_mask)
        mask_threating_the_king_hypoth = self.f_threat_mask_allpieces (np_board, color_of_mask)
        print(f'mask_threating_the_king actual vs hypoth: \n {np.where(mask_threating_the_king_actual != mask_threating_the_king_hypoth)}')
        
        return mask_threating_the_king_hypoth, loc_king;


    #%% everything related to check condition
    
    def king_will_still_be_checked_after_this_move (self, curr_np_board, color_of_king, move_from_row, move_from_col, move_to_row, move_to_col):
        
        """ returns True if king will still be in check after a piece move 
            assumption. king is already in check! """

        king_is_still_checked = True
        mask_threating_the_king_hypoth, loc_king = self.calc_hypoth_mask (curr_np_board, color_of_king, move_from_row, move_from_col, move_to_row, move_to_col)
        
        # did this hypothetical move of a piece, save the king? 
        if mask_threating_the_king_hypoth [loc_king[0], loc_king[1]] == 0:
            king_is_still_checked = False
            
        # if not, it was an INVALID move, so dont do anything, do not actually move that  piece
        elif mask_threating_the_king_hypoth [loc_king[0], loc_king[1]] == 1:
            print(f'{color_of_king} king is still checked! make a move to resolve the check.')
        
        return king_is_still_checked
                       
    
    def king_will_be_checked_after_this_move (self, curr_np_board, color_of_king, move_from_row, move_from_col, move_to_row, move_to_col):
        
        """ returns True if king will be in check after a (hypothetical) piece move 
            assumption. king is NOT already in check! """
        
        king_will_be_checked = False
        mask_threating_the_king_hypoth, loc_king = self.calc_hypoth_mask (curr_np_board, color_of_king, move_from_row, move_from_col, move_to_row, move_to_col)
        
        # will this hypothetical move of a piece, will put the king in check condition? => this is an invalid move, do not allow it
        if mask_threating_the_king_hypoth [loc_king[0], loc_king[1]] == 1:
            king_will_be_checked = True
            print(f'invalid move: if you make this move, your king: {color_of_king} will be checked!')
            
        # if this hypothetical move will not endanger the king, then its a valid move, allow it
        elif mask_threating_the_king_hypoth [loc_king[0], loc_king[1]] == 0:
            print(f'valid move: if you make this move, your king: {color_of_king} will NOT be checked!')
              
        return king_will_be_checked
        
        
    # check
    def f_king_is_checked (self, curr_np_board, color_of_king):
        
        """ returns True if the king is in check!"""
        
        king_is_checked = False
        
        if color_of_king == 'white':
            mask_threating_the_king = self.f_threat_mask_allpieces (curr_np_board, 'black')
            loc_king = np.where(curr_np_board == 6)
            # print(f'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \n mask_threating_the_white_king  \n {mask_threating_the_king}')
        elif color_of_king == 'black':
            mask_threating_the_king = self.f_threat_mask_allpieces (curr_np_board, 'white') 
            loc_king = np.where(curr_np_board == -6)
            
        if mask_threating_the_king [loc_king[0], loc_king[1]] == 1:
            king_is_checked = True
            # print('king is checked!')
        
        return king_is_checked
     
       
    #%% stalemate
    
    def f_stalemate (self, curr_np_board, color_of_king):
        
        """ returns True if stalemate happens """
        
        # Stalemate happens when a player is not in check but can't make a legal move. 
        # stalemate ends in a draw (neither of the players wins or loses) or tie (equal win: each player wins half a point).
        
        stalemate = False
        
        if color_of_king == 'white':
            loc_king = np.where(curr_np_board == 6)
        elif color_of_king == 'black':
            loc_king = np.where(curr_np_board == -6)
        row_king = loc_king[0][0]
        col_king = loc_king[1][0]
        
        move_mask_kk = self.f_move_mask_kk (curr_np_board, row_king, col_king, include_the_king_in_mask_calc = False)
        threat_mask_allpieces = self.f_threat_mask_allpieces (curr_np_board, color_of_king)
        if self.is_debug:
            print(f' *** all_locations_to_which_{color_of_king}_king_can_go: *** \n {move_mask_kk}')
            print(f' *** all_locations_to_which_{color_of_king}_can_go REGARDLESS of check or stale condition: *** \n {threat_mask_allpieces}')
            
        # (1): check if ALL elements of move_mask_kk array are equal to zero => king cannot go anywhere
        # no_valid_move_is_possible_for_king = all(v == 0 for v in np.nditer(move_mask_kk))
        
        # (2): check if ALL elements of threat_mask_allpieces array are equal to zero (except for locations, to which king can go) 
        #   => no other piece can go anywhere either
        # no_valid_move_is_possible_for_anypiece_but_king = ...
       
        # (1) + (2) = stalemate condition
        threat_mask_allpieces_including_the_king = np.multiply (move_mask_kk, threat_mask_allpieces)
        # print(f' *** threat_mask_allpieces_including_the_king: \n np.multiply (move_mask_kk, threat_mask_allpieces) *** \n {threat_mask_allpieces_including_the_king}')
        no_valid_move_is_possible_for_anypiece = all(v == 0 for v in np.nditer(threat_mask_allpieces_including_the_king))

        if no_valid_move_is_possible_for_anypiece:
            stalemate = True
    
        return stalemate
    
    #%% Checkmate   
        
    def f_checkmate (self, curr_np_board, color_of_king):
        
        """ returns True if checkmate happens """
        
        # checkmate happens when 
        
        checkmate = False
        
        if color_of_king == 'white':
            loc_king = np.where(curr_np_board == 6)
        elif color_of_king == 'black':
            loc_king = np.where(curr_np_board == -6)
        row_king = loc_king[0][0]
        col_king = loc_king[1][0]
        
        
        king_is_checked = self.f_king_is_checked (curr_np_board, color_of_king)
        move_mask_kk = self.f_move_mask_kk (curr_np_board, row_king, col_king, include_the_king_in_mask_calc = False)
        threat_mask_allpieces = self.f_threat_mask_allpieces (curr_np_board, color_of_king)
        
        # if self.is_debug:
        print(king_is_checked)
        # print(f' *** move_mask_kk for {color_of_king} king: *** \n {move_mask_kk}')
        # print(f' *** threat_mask_allpieces for {color_of_king} color: *** \n {threat_mask_allpieces}')
        print(f' ===== all_locations_to_which_{color_of_king}_king_can_go: ===== \n {move_mask_kk}')
        print(f' ===== all_locations_to_which_{color_of_king}_can_go REGARDLESS of check or stale condition: ===== \n {threat_mask_allpieces}')
        
        
        threat_mask_allpieces_including_the_king = np.multiply (move_mask_kk, threat_mask_allpieces)
        # print(f' *** threat_mask_allpieces_including_the_king: \n np.multiply (move_mask_kk, threat_mask_allpieces) *** \n {threat_mask_allpieces_including_the_king}')
        no_valid_move_is_possible_for_anypiece = all(v == 0 for v in np.nditer(threat_mask_allpieces_including_the_king))
        
        if king_is_checked and no_valid_move_is_possible_for_anypiece:
            checkmate = True
        
        
        return checkmate
        
        
        
        
        
        
        
        
    
    
