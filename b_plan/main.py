from game_engine.game_engine import *
from graphic_engine import main as gp
import pygame

class MainGame():
    WIDTH, HEIGHT = 1200, 750 

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.game_engine = Game()
        self.game_data = None


    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((0, 0, 0))
            keys = pygame.key.get_pressed()
            self.game_data = self.game_engine.get_game_data()

            if keys[pygame.K_SPACE] and self.game_data.get("game").get("state") == 0:
                self.game_engine.waiting_state(player_input="space")
            
            elif self.game_data.get("game").get("state") == 1:

                if keys[pygame.K_a]:
                    self.game_engine.playing_state(player_id=1, player_input="left")
                if keys[pygame.K_d]:
                    self.game_engine.playing_state(player_id=1, player_input="right")
                if keys[pygame.K_LEFT]:
                    self.game_engine.playing_state(player_id=2, player_input="left")
                if keys[pygame.K_RIGHT]:
                    self.game_engine.playing_state(player_id=2, player_input="right")
                self.game_engine.update()

            # Render everything
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def draw(self):
        self.game_data = self.game_engine.get_game_data()
        
        # extract players
        players = self.game_data.get("players")
        player1_segments = players.get("player1").get("segments")
        player1_style = gp.PlayerGraphicBasic(player1_segments, screen=self.screen)
        player2_segments = players.get("player2").get("segments") 
        player2_style = gp.PlayerGraphicBasic(player2_segments, screen=self.screen)
        player1_color = players.get("player1").get("color")
        player2_color = players.get("player2").get("color")
        player1_score = players.get("player1").get("score")
        player2_score = players.get("player2").get("score")
        
        # extract scores
        fruits = self.game_data.get("fruits")
        apples_position = fruits.get("position")
        apples_scores = fruits.get("score")
        
        # draw_player
        for i, ele in enumerate(player1_segments):
            pygame.draw.circle(self.screen,
                               center=ele[0],
                               color=player1_color[i],
                               radius=ele[1])
        player1_style.body_draw(color=player1_color[0])
        
        for i, ele in enumerate(player2_segments):
            pygame.draw.circle(self.screen,
                               center=ele[0],
                               color=player2_color[i],
                               radius=ele[1])
        player2_style.body_draw(color=player2_color[0])
            
        
        # draw apples
        for i, ele in enumerate(apples_position):
            pygame.draw.circle(self.screen,
                               center=ele[:2],
                               color=ele[2],
                               radius=9)
            pygame.draw.circle(self.screen,
                               center=ele[:2],
                               color="white",
                               radius=4)
            
        # Draw Score Board
        font = pygame.font.SysFont(None, 32)
        score1 = font.render(f"Player1 : {player1_score}", True, "white")
        score2 = font.render(f"Player2 : {player2_score}", True, "white")
        self.screen.blit(score1, (10, 10))
        self.screen.blit(score2, (1000, 10))

        if self.game_data.get("game").get("state") == 0:
           waiting = font.render("Press ENTER to start", True, "white") 
           self.screen.blit(waiting, (500, 500))


if __name__ == "__main__":
    game = MainGame()
    game.run()