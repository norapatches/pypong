# pypong
The popular video game PONG implemented in Python using the PyGame library.

# game modes
- 1PvsCPU:  play against the computer
- 1Pvs2P:   play against another player

# controls
- **W and S keys:**       Move Player 1 up and down
- **UP and DOWN arrows:** Move Player 2 up and down
- **SPACEBAR:**           Pause/unpause the game
- **ESCAPE:**             Quit the game

# game logic
Each player (even the CPU) gets one point for successfully blocking the ball. The ball speed is incremented after each fifth blocking of the ball by any player.
Each player can grow in size after each tenth individual blocking of the ball.
If the ball hits the left or right sides of the screen, that player loses the game.
