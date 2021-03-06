import blahajIkea
import highScore
import homeScreen
import titleScreen

# add title screen
titleScreen.run_title()

while True:
    # show home screen
    # home screen returns a value
    game_selected = homeScreen.run_homescreen()

    # if home screen select is game, run the blahaj game
    # opens the blahaj game window
    if game_selected:
        blahajIkea.runBlahajGame()

    # if home screen select is high scores, run high score screen
    else:
        highScore.run_highscore()
