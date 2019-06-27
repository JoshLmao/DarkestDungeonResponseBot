<h1>
  <br>
  Darkest Dungeon Response Bot
  </br>
</h1>

<p align="right">
  <img src="https://i.imgur.com/h7XUiDU.png" width="175px" align="right"></img>
</p>

<p>
  <a href="https://twitter.com/JoshLmao">
    <img src="https://img.shields.io/badge/twitter-JoshLmao-blue.svg?style=flat-square" alt="twitter"/>
  </a>
  <a href="https://ko-fi.com/joshlmao">
    <img src="https://img.shields.io/badge/support-ko_fi-orange.svg?style=flat-square" alt="twitter"/>
  </a>
  <a href="https://reddit.com/r/darkestdungeon">
    <img src="https://img.shields.io/badge/live-/r/DarkestDungeon-success.svg?style=flat-square" alt="twitter"/>
  </a>
</p>

A simple Reddit bot created using Python 3.6 to respond to recent Reddit comments in a certain subreddit. The bot looks for phrases and voice lines from the Darkest Dungeon's Narrator.

All responses can be found in the [responses.json](./responses.json) file or on the [Narrator's Gamepedia page](https://darkestdungeon.gamepedia.com/Narrator). Massive thanks to the creators and maintainers of [the Darkest Dungeon Gamepedia](https://darkestdungeon.gamepedia.com) for organizing and sorting his voice lines

## How it works

The bot scans recent /hot/ and /new/ threads in a subreddit (set in [responses_constants](./responses_constants.py) file) for comments that are meant to match a voice line of the Narrator. Both the comment and database description strings are cleaned before comparing for a match, which means **punctuation** and even **emojis** don't affect the bot 😂😂👍👌🔥

## Problems

Any problems with the bot, please use the [Issues tab](https://github.com/JoshLmao/DarkestDungeonResponseBot/issues) and/or send me a Tweet [@JoshLmao](https://twitter.com/JoshLmao)