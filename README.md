Euchre Sim
=============

It's a simple euchre simulation intended for AI competition.  It's not exactly brilliantly designed, but everything that needs to be there is there, and if you're familiar with the game, it should be straightforward to build a player.  To build a player, subclass the Player class and override the following five functions (two are somewhat optional, as they are only messages that don't require action):

- **call()**: The basic means of playing a card during a trick.
- **action()**: Calling trump by telling the dealer to "pick it up" or calling a suit
- **discard()**: Discard if you're the deal and pick up the face-up card
- **end_call()** (optional): See who ended up calling what
- **end_trick()** (optional): See who won the trick and what cards were played


Dependencies
------------

Unicard
