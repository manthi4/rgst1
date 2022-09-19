ReadMe.md
# An interface to present output from other projects in a personable way.
## Version control stuff
*  to download required python packages run ```pip install -r reqs.txt```
*  to create reqs.txt run ```pip freeze > reqs.txt```
## Libraries of interest
*   https://betterprogramming.pub/5-python-libraries-for-better-console-output-b2494b587855
*   climage
*   Curses!
*   Urwid
*   gif-for-cli

## Next steps
*   change git accounts using visual studio
*   start testing on wsl
## gif-for-cli
*   Run ```gif-for-cli ./sime2.gif``` or ```gif-for-cli "anime"```

## Curses !!!
* What is getch?    
  * get charecter (user input)
* curses.noecho()
   * Gotta use this to make sure the program doesn't close when user input is detected
* curses.endwin()
  * manually kill the program (if you called noecho)
* wrapper(main)
  * A very useful import from curses that can wrap your main and do a bunch of useful background inits and handling automatically
* curses.LINES - 1, curses.COLS - 1)
  * terminal window h and w
