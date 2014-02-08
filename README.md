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

Also available to the player are the following functions called on the Game object (to prevent tampering), which return info about the player's current state:

- ```self.game.hand_for(self)```: Available cards to play at that moment
- ```self.game.position_for(self)```: Permanent position at table for the game
- ```self.game.team_num_for(self)```: Team number
- ```self.game.is_player_active(self)```: True if player has not been told its teammate wants to go alone

Any MyPlayer implementation that wants to keep track of cards played over time should implement its own storage to be used with the ```end_trick()``` callback.  ```utils``` also has some functions that help with manipulation of cards.

Dependencies
------------

[Unicards](https://github.com/lmacken/unicards) may be added to make for prettier printing.

TODOs
-----

- This should seriously have some test coverage.