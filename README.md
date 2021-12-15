# VisualizationProject - Chess
This project shows how different visualization techniques can help understand games. The analysis is over 7000 games by Magnus Carlsen (current world champion), which were obtained from [here](http://smallchess.com/Games/).

## Task 1. Visualize the average color of the piece at every square

In this task, if a given square (e.g. the first square is **a1**) had white piece for 20/40 turns, a black piece for 10/40 turns, and no piece for 10/40 turns, it would get a score of +10, whereas if it had a black piece for 20/40 turns, a white piece for 10/40 turns and no piece for 10/40 turns, it would get a score of -10. The first game would then result in the following plots. Notice how choosing a diverging colormap (red representing the player using white pieces and blue representing the player using black pieces) it tells us information about which player had control of any given square.

<img width="400" alt="First game square color" src="https://github.com/rm36/VisualizationProject/blob/main/output/first_game_square_color_2d.png?raw=true"> <img width="420" alt="First game square color diverging" src="https://github.com/rm36/VisualizationProject/blob/main/output/first_game_square_color_2d_seismic.png?raw=true">

In the second plot we can see that the square **c1** was controlled by a black piece for longer than a white piece.

When doing the analysis over the 700 games by Magnus in the database, we get interesting overall statistics. For example, that the squares **b4** and **g5** have relatively the same time controlled by either color. Also, plotting it in 3D can show better small differences on each square such as **f7** and **g7**, which are very difficult to notice the color differences in the 2D plot. 

<img width="420" alt="All games square color" src="https://github.com/rm36/VisualizationProject/blob/main/output/all_games_square_color_2d_seismic.png?raw=true"> <img width="380" alt="All games square color 3D" src="https://github.com/rm36/VisualizationProject/blob/main/output/all_games_square_color_3d.png?raw=true">

## Task 2. Visualize the average color that attacks each square

Another way to define "controlling" a square is by being able to capture that square. So a square would have a score of +1 on a turn when a white piece could capture a black piece on that square, -1 on a turn when a black piece could capture a white piece on that square, and 0 if none or both colors could capture that square. Here is the result of the analysis for all games.

<img width="420" alt="All games square attack" src="https://github.com/rm36/VisualizationProject/blob/main/output/all_games_square_attack_2d_seismic.png?raw=true"> <img width="380" alt="All games square attack 3D" src="https://github.com/rm36/VisualizationProject/blob/main/output/all_games_square_attack_3d.png?raw=true">

Notice how the **b4**, **c5**, **f5** and **g4** are "controlled" by black, since it aligns diagonally where the bishops are (**c8** and **f8**) and similarly for white. Also, the 3 ranks on each side are controlled by the color very clearly, whereas the middle ranks are contested.

## Task 3. Piece movement

The following plot shows the total movement (in king steps) that a piece does over a game. For the first game we have the following plots, both in linear and logarithmic scale. Notice how log is much better because one piece moved much more than all the other ones in the game.

<img width="400" alt="First game piece movement linear" src="https://github.com/rm36/VisualizationProject/blob/main/output/first_game_movement_2d_linear.png?raw=true"> <img width="400" alt="First game piece movement log" src="https://github.com/rm36/VisualizationProject/blob/main/output/first_game_movement_2d_log.png?raw=true">

And now the plots for the average per-game piece movement for all games.

<img width="420" alt="All games piece movement" src="https://github.com/rm36/VisualizationProject/blob/main/output/all_games_average_movement_2d_linear.png?raw=true"> <img width="380" alt="All games piece movement 3D" src="https://github.com/rm36/VisualizationProject/blob/main/output/all_games_average_movement_3d.png?raw=true">

Notice how while the 3D plot occludes visibility, the actual values are easier to read from that plot, and it's also easier to measure the relative difference in movement. One learning from the 2D plot is that the 3 pawns in files **c**, **d** and **e** move more than all the others, which makes sense because they're in the center and they don't weaken the king (like **f** pawns do when they move early).

## Task 4. Piece tension

We define tension when a piece can be captured in a given turn but isn't. These plots add up the number of turns they were in "tension".

<img width="420" alt="All games piece movement" src="https://github.com/rm36/VisualizationProject/blob/main/output/all_games_tension_2d_log.png?raw=true"> <img width="380" alt="All games piece movement 3D" src="https://github.com/rm36/VisualizationProject/blob/main/output/all_games_tension_3d.png?raw=true">

Notice how:
- The pawns had the most turns in tension
- The **e** pawns, which are in front of the kings, had the most tension
- The king wasn't ever in tension (that would be checkmate, by definition)
- The queen was very rarely in tension, probably because is the most valuable piece
- The rooks and knights (e.g. **a1** and **c1**) are in tension less time in average than the bishops.
