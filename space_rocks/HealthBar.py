import pygame

class HealthBar():
    """
    A class to represent the health of the ship on the screen
    
    Attributes
    ----------
    __healthBar : pygame.Rect
    __healthBarColor : Tuple
    __healthBarBGColor : Tuple
    __healthBarBG : pygame.Rect
    __font : pygame.font
    __healthText : font.Render
    
    Methods 
    -------
    draw(screen) 
        draws the healthbar on the screen
    update(health)
        updates the health of the ship
    
    """
    def __init__(self,screen):
        """
        Parameters
        -----------
            screen : pygame.display
        """
        self.__healthBar = pygame.Rect(screen.get_width()-120, 30, 100, 15)
        self.__healthBarColor = (0,255,0)
        self.__healthBarBGColor = (255,0,0)
        self.__healthBarBG = pygame.Rect(screen.get_width()-120, 30,100,15)
        self.__font = pygame.font.Font('Fonts/Lora-Bold.ttf', 20)
        self.__healthText = self.__font.render("HEALTH", 1, (255,255,255))
    def draw(self, screen):
        """
        draws the healthbar on the screen
        
        Parameters
        ----------
            screen : pygame.display
        """
        screen.blit(self.__healthText,(screen.get_width()-111, 5))
        pygame.draw.rect(screen, self.__healthBarBGColor, self.__healthBarBG)
        pygame.draw.rect(screen, self.__healthBarColor, self.__healthBar)
        
    def update(self, health):
        """
        updates the health of the ship
        Args:
            health (_type_): _description_
        """
        self.__healthBar.width = health