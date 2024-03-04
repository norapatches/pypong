# pyPong
The popular video game PONG implemented in Python using the PyGame library.

Play against the computer or against a friend!

## game modes
1. **1P vs CPU:**  play against the computer
2. **1P vs 2P:**   play against another player

## controls
- **W and S keys:**       Move Player 1 up and down
- **UP and DOWN arrows:** Move Player 2 up and down
- **SPACEBAR:**           Pause/unpause the game
- **ESCAPE:**             Quit the game

### game logic
Each player (even the CPU) gets one point for successfully blocking the ball.

The ball speed is incremented after each fifth contact with any player.

Each player can grow in size after each tenth individual blocking of the ball.

If the ball hits the left or right sides of the screen, that player loses the game.

#### created by
Norbert Kovács-Wilczyński in March 2024
version 0.2