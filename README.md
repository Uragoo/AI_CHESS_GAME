# AI_CHESS_GAME
## AI chess game using python and pygame for a school project

* Entry point is main.py
* Press 'r' to reset the game
* Press the right arrow to undo moves
* By default, the game is in Player vs AI mode, we didn't have the time to create a menu so if you want to change this mode, you can just modify the boolean variable in main.py on line 22 and 23
* If you play in AI vs AI mode, please press the right arrow for each turn

Improvement ideas :
- A mode select menu to change between Player vs Player, Player vs AI and AI vs AI
- Multiple themes
- Sounds
- End of the game state/menu
- End of the game with draw (3 moves repetition, 50 moves draw)
- Add openings database so the AI does not need to recalculate positions each start of the game
- Save previous calculated positions and use them instead of recalculating all moves
- Use Zobrist hashing to reduce conputing time (to complex for us in the time given)
- Improve the scoring system of the game to make the AI smarter like giving more weight to tiles threatening the most enemies or defending the most allies

Known issues :
- Some issues with checks => the king sometimes behave like he is in a check situation wile it's not the case
- The AI is relatively slow given the combination number in the game. With more time, we would have try to implement new way of saving AI calculations to reuse them istead of recalculate every moves
- The AI is also not the smartest

End words :
* Working on the project was really fun : trying to recreate a classic game such as chess was hard but also very rewarding.
* We hope you will find our work as satisfying as we worked hard on thi
