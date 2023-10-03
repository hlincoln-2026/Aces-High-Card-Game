###############################################################################
###
#
#                               Project 10
#
#       Import cards module
#       Initalize constants
#       Define function
#
#       Main function
#           Display rules and menu
#           Initalize game with functions
#           Prompt user for option selection
#           If option == D
#               Use functions to deal to the tableau
#           If option == F
#               Use function to move card to foundation
#           If option == T
#               Use functions to move card between columns in the tableau
#           If option == R
#               Restart the game to a fresh game
#           If option == H
#               Redisplay menu and current game standing
#           If option == Q
#               Quit game and display message that user has quit the game
#
#           When the user wins the game, the program will 
#           displaying winning message and end the program
#
###
###############################################################################


import cards  # required !!!

RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card 
     of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.'''

MENU = '''     
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''

def init_game():
    '''
    Inputs: None
    Actions: Shuffles a deck of cards, then makes a tableau and empty foundation with cards
    Returns: Shuffled deck, tableau, and foundation
    '''
    # Gets deck of cards and shuffles them
    stock = cards.Deck()
    stock.shuffle()
    
    tableau = [[],[],[],[]]  # Empty list with four columns represented by a list
    # For each column in tableau
    for col in tableau:
        # Add a card
        col.append(stock.deal())
            
    foundation = []  # Empty list for foundation
    
    # Returns all the data structures
    return (stock, tableau, foundation)
                               
    
def deal_to_tableau( tableau, stock):
    '''
    Inputs: Tableau and deck of cards
    Actions: Deals cards to each column of tableau
    Returns: Nothing
    '''
    # For each column in tableau
    for col in tableau:
        # Try adding a card from the deck
        try:
            col.append(stock.deal())
        # If there isn't a card to deal
        except:
            # Break from the loop
            break
    # Return tableau        
    return (tableau)

           
def validate_move_to_foundation( tableau, from_col ):
    '''
    Inputs: Tableau and column number
    Actions: Checks to see if moving the last card from the specified column to the foundation is possible
    Returns: True or False based on possibity of movement to foundation
    '''
    
    try:
        # Gets the rank of the card from the specified column
        test_rank = tableau[from_col][-1].rank()
        # If the card is an ace, turn the rank to 14 making ace high instead of low
        if test_rank == 1:
            test_rank = 14
        # Gets the suit of the card from the specified column
        test_suit = tableau[from_col][-1].suit()
        highest = 0  # Established base value for highest
        # Loops through each column in the Tableau
        for index, col in enumerate(tableau):
            # If the column is the spcified column and is empty
            if index == from_col and col == []:
                # Raise an error
                raise IndexError
            # If the column is just empty
            elif col == []:
                # Skip the column
                pass
            # If the column has cards
            else:
                # Get the rank of the last card in the column
                rank = col[-1].rank()
                # If the card is an ace, turn the rank to 14 making ace high instead of low
                if rank == 1:
                    rank = 14
                # Get the suit of the last card in the column
                suit = col[-1].suit()
                # If the column is the specified column
                if col == from_col:
                    # Skip the column
                    pass
                else:
                    # If the card has the same suit as the last card from the specifed column
                    if test_suit == suit:
                        # If the rank of the card is the highest
                        if rank > highest:
                            # Set new highest
                            highest = rank
        # If the specified column's card is lower then the highest card of that suit
        if test_rank < highest:
            # Return true
            return True
        # Otherwise
        else:
            # Display error and return false
            print("\nError, cannot move {}.".format(tableau[from_col][-1]))
            return False
        
    # If IndexError is raised or occures
    except IndexError:
        # Display error and return false
        print("\nError, empty column: {}".format(from_col+1))
        return False


def move_to_foundation( tableau, foundation, from_col ):
    '''
    Inputs: Tableau, foundation, and column number
    Actions: Moves a card from the tableau to the foundation
    Returns: None
    '''    
    # Gets a true or false value for if a move is valid
    valid = validate_move_to_foundation(tableau, from_col)
    # If the move is confirmed valid
    if valid == True:
        # Add the card to the foundation
        foundation.append(tableau[from_col][-1])
        # Remove the card from the column in th tableau
        tableau[from_col].pop(-1)


def validate_move_within_tableau( tableau, from_col, to_col ):
    '''
    Inputs: Tableau, column number to take from, and column number to move to
    Actions: Determains if a card move from one column to another is valid
    Returns: True or False based on if move is valid
    '''
    # Gets the starting and ending columns from the tableau
    start_col = tableau[from_col]
    end_col = tableau[to_col]
    
    # If both columns are empty
    if len(start_col) == 0 and len(end_col) == 0:
        # Display appropriate error message and return False
        print("\nError, no card in column: {}".format(from_col + 1 ))
        return False
    # If only the ending column is empty
    if len(end_col) == 0:
        # Return True which validates the move
        return True
    # If aything else occurs
    else:
        # Display error message and return False
        print("\nError, target column is not empty: {}".format(to_col + 1 ))
        return False
    

def move_within_tableau( tableau, from_col, to_col ):
    '''
    Inputs: Tableau, and two column indices
    Actions: Moves a card between columns in the tableau
    Returns: None
    '''
    
    # Check is the move is valid
    valid = validate_move_within_tableau(tableau, from_col, to_col)
    # If the move is valid
    if valid == True:
        # Add the card from the starting column to the new column
        tableau[to_col].append(tableau[from_col][-1])
        # Remove the card from the starting column
        tableau[from_col].pop(-1)
    
        
def check_for_win( tableau, stock ):
    '''
    Inputs: Tableau and stock
    Actions: Checks if the stock is empty and only aces are present in tableau
    Returns: True if it meets both checks and False if otherwise
    '''
    # Checks if the stock is empty
    if len(stock) == 0:
    
        count = 0  # INtitalize count to track number of cards above an ace
        # Loops through each column in tableau
        for col in tableau:
            # Loops through each card in column
            for card in col:
                # If the card is not an ace
                if card.rank() != 1:
                    # Increase count by 1
                    count += 1
        # If count shows there are not only aces
        if count != 0:
            # Return False
            return False
        # IF only aces appear
        else:
            # Return True
            return True
        
    # If stock still has cards
    else:
        # Return False
        return False
    

def display( stock, tableau, foundation ):
    '''Provided: Display the stock, tableau, and foundation.'''

    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))
    maxm = 0
    for col in tableau:
        if len(col) > maxm:
            maxm = len(col)
    
    assert maxm > 0   # maxm == 0 should not happen in this game?
        
    for i in range(maxm):
        if i == 0:
            if stock.is_empty():
                print("{:<8s}".format(""),end='')
            else:
                print("{:<8s}".format(" XX"),end='')
        else:
            print("{:<8s}".format(""),end='')        
        
        #prior_ten = False  # indicate if prior card was a ten
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print( "{:4s}".format( str(col[i]) ), end='' )

        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')
                
        print()


def get_option():
    '''
    Inputs: None
    Actions: Displays options and gets user input, then makes a list of the users input
    Returns: List containing user input
    '''
    
    return_list = []  # Empty list to add letter and values that user inputs
    options = ['D','F','T','R','H','Q']  # List of possible valid user inputs
    
    # Gets user input
    selection = input("\nInput an option (DFTRHQ): ")
    upper_selection = selection.upper()
    # If user input is in the list of possible options    
    if upper_selection[0].upper() in options:
        upper_selection = upper_selection.upper()
        
        if upper_selection[0] == 'D' and len(upper_selection) > 1:
            print("\nError in option: {}".format(selection))
            return []
        
        
        # If seletion is 'F' or 'T'
        if upper_selection[0] == 'F' or upper_selection[0] == 'T':
            
            if upper_selection[0] == 'T' and len(upper_selection) < 5:
                print("\nError in option: {}".format(selection))
                return []
            
            if upper_selection[0] == 'F' and len(upper_selection) < 3:
                print("\nError in option: {}".format(selection))
                return []
            
            # Split the input into a list
            temp_list = upper_selection.split(' ')
            # Loop through each value in the list
            for i in temp_list:
                if i.isdigit() and ( int(i)> 4 or int(i) < 1):
                    print("\nError in option: {}".format(selection))
                    return []
                # If the value is a number
                if i.isdigit():
                    # Turn the value into an integer
                    i = int(i) - 1
                # Add the value to the return list
                return_list.append(i)
            
        # If the selection is any other valid selection
        else:
            # Add the selection to the return list
            return_list.append(upper_selection)
    # If input not valid option
    else:
        # Display error and return an empty list
        print("\nError in option: {}".format(selection))
    # Returns list containg option
    return return_list

        
def main():
    # Display rules and menu
    print(RULES)
    print(MENU)
    
    # Initalize the game
    stock, tableau, foundation = init_game()
    # Display current state of game
    display(stock, tableau, foundation)
    
    
    
    
    # Get user option choice
    option = get_option()
    # Loop unitl the user selects option 'Q'
    while option != ['Q']:
        
        if option == []:
            pass
        
        # If option choice is D
        elif option[0] == 'D':
            # Deals 4 cards to tableau
            deal_to_tableau(tableau, stock)
            # Displays current state of game
            display(stock, tableau, foundation)
            
        # If option choice is F
        elif option[0] == 'F':
            # Moves the card is move is valid or displays an error message
            move_to_foundation(tableau, foundation, option[1])
            # Checks for win
            win = check_for_win(tableau, stock)
            if win == True:
                break
            else:
                # Displays current state of game
                display(stock, tableau, foundation)
            
        # If option choice is T
        elif option[0] == 'T':
            
            # Moves card within the tableau if move is valid or displays error message
            move_within_tableau(tableau, option[1], option[2])
            # Checks for win
            win = check_for_win(tableau, stock)
            if win == True:
                break
            else:
                # Displays current state of game
                display(stock, tableau, foundation)
            
            
           
        # If option choice is R
        elif option[0] == 'R':
            # Display retarting
            print("\n=========== Restarting: new game ============")
            # Redisplay menu and rules
            print(RULES)
            print(MENU)
            # Initalize new game
            stock, tableau, foundation = init_game()
            display(stock, tableau, foundation)
        
        # If option selected is 'H'
        elif option[0] == 'H':
            # Redisplay the menu
            print(MENU)
            display(stock, tableau, foundation)
            
        # If option choice is not a valid choice
        else:
            # Skip to repromting for option
            pass
        
        
        
        # Get user option choice
        option = get_option()
        
        
        
        
    
    
    # Checks for win
    win = check_for_win(tableau, stock)
    if win == True:
        # Display win message
        print("\nYou won!")
        
    
    else:
        # When user selects the option to quit display message
        print("\nYou have chosen to quit.")
    

if __name__ == '__main__':
     main()
