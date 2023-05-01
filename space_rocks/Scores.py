import pygame
    
class Scores():
    """
    A class to show the scores of the players in the game
    ...
    
    Attributes
    ----------
    font : pygame.font
    user : list
    
    Methods
    -------
    addPlayer(Id, color)
        appends a player to the list of users with an Id and color
    update(Id, score)
        updates the score of the player with the given Id
    draw(screen)
        draws the scoreboard on the screen
    
    """ 
    def __init__(self, player, color):
        """
        Parameters
        ----------
            player : string
            color : rgb value
        """
        
        self.__font = self.font = pygame.font.Font(None, 20)
        self.__font.set_underline(1)
        self.__italic = self.font = pygame.font.Font(None, 18)
        self.__user = []
        self.addPlayer(player, color)
        
    def addPlayer(self, Id, color):
        """
        adds a player to a list of users in the game
        
        Parameters
        ----------
            Id : string
            color : rgb value
        """
        self.__user.append([Id,0, color])

    def update(self, Id, Score):
        """
        updates the score of each player according to their Id 
        and sorts the scores fomr highest to loweest

        Parameters
        ----------
            Id : string
            Score : int
        """
        for tup in self.__user:
            if tup[0] == Id:
                tup[1] = Score
                self.__user.sort(key=lambda tup: tup[1], reverse=True)
                break
        
    def draw(self, screen):
        """
        draws the Score Board on the screen 

        Parameters
        ----------
            screen : pygame.display
        """
        screen.blit(self.__font.render("SCORE BOARD", 1, (255,255,255)), (15, 5))
        pos = 28
        for player in self.__user:
            screen.blit(self.__italic.render(str(player[0]) +": "+ str(player[1]), 1, player[2]), (15,pos))
            pos += 22
        