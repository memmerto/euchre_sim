Euchre Sim
=============

It's a simple euchre simulation intended for AI competition.  It's not exactly brilliantly designed, but everything that needs to be there is there, and if you're familiar with the game, it should be straightforward to build a player.  To build a player, subclass the Player class and override the following five functions (two are somewhat optional, as they are only messages that don't require action):

- ```call()```: The basic means of playing a card during a trick.
- ```action()```: Calling trump by telling the dealer to "pick it up" or calling a suit
- ```discard()```: Discard if you're the dealer and pick up the face-up card
- ```end_call()``` (optional): See who ended up calling what
- ```end_trick()``` (optional): See who won the trick and what cards were played

A skeleton for such a subclass is provided (MyPlayer).  The Player class itself implements the most simple legal versions of each function (they're not very smart).  In the implementaion of these five methods, MyPlayer may access info about the game by checking the following properties:

- ```self.game.topcard```: The face up card that showed during the calling portion of the hand
- ```self.game.trump```: Trump for the current hand
- ```self.game.caller_pos```: Position of the player who called trump for current hand
- ```self.game.tricks_score```: A dict of the number of tricks won by each team for current hand, like {1: 3, 2: 2}
- ```self.game.game_score```: A dict of the total game score for each team, like {1: 8, 2: 9}

Any MyPlayer implementation that wants to keep track of cards played over time should implement its own storage to be used with the ```end_trick()``` callback.  ```utils``` also has some functions that help with manipulation of cards.

A reasonable effort has been made to encapsulate info used to make the Game run correctly, but there are security holes that should be closed.  For now, it should be expected that the player does not modify its own attributes: ```self.team_num```, ```self.hand```, ```self.position```, ```self.active```.

Things like ```self.position```, ```self.team_num```, and ```self.active``` are not used by the Game client, so if a player changes them for some reason, the client won't be affected.


Dependencies
------------

[Unicards](https://github.com/lmacken/unicards) may be added to make for prettier printing.

TODOs
-----

- Each player's hand should be kept track of by the Game client for security reasons, and every card coming from a player's hand should be validated.
- This should seriously have some test coverage.