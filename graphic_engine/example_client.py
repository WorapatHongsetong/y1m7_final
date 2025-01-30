"""
Feature
- Render Snakes         Ver 1   Useable
                                            Legs
                                            Laser
- Render Fruits         Ver 1   Useable         
                                            Special Fruits
"""


import main as gp

GRAPHIC = gp.GameEngine((800,600))  # You can change screen size, all render will change relative to screen size


# Player position (x, y, r)
EXAMPLE_CHAIN = [(100, 150, 50), (200, 170, 45), (300, 180, 35), (400, 200, 20)]

# Create player
PLAYER1 = gp.PlayerGraphicBasic(EXAMPLE_CHAIN, GRAPHIC.screen)
# PLAYER2

# ADD TO PLAYER LIST
PLAYER_LST = [PLAYER1]

# Create fruits
FRUITS_LST = gp.Fruits([(6, 9), (20, 12), (32, 64)], GRAPHIC.screen)

# REGISTER DATA TO GRAPHIC ENGINE
GRAPHIC.reg_players(PLAYER_LST)
GRAPHIC.reg_fruits(FRUITS_LST)

# RUN
GRAPHIC.run()