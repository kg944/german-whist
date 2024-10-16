# [WIP] German Whist
This is a python cli version of the two player game, [German Whist](https://en.wikipedia.org/wiki/German_whist). Currently still in progress, but when done will have a semi-competent AI to play against.

## Tasks
### In Progress

### TODO
1. fix Ace ranking
1. support bots playing each other
1. unit tests
1. update UI to look like a card game

### Done
1. card object
1. game init
1. turn functionality
1. card comparison logic
1. add opponent card playing logic
 1. add logic to not allow trump suit unbroken
 1. add logic to not allow not following suit
1. add breaking trump suit
1. validate user input
1. add battle stage logic

## AI
A longer term goal would be to experiment with various AI improvements and pit each version against each other to compare the improvements of each, in order to judge the effectiveness of each addition -- this is inspired by [Sebastion Lague's](https://github.com/seblague) video creating [chess bots](https://youtu.be/_vqlIPDR2TU?t=2743). 

Not sure yet how many German Whist / card game AI strategies and documentation exists (compared to the vast [chess ai resources](https://www.chessprogramming.org/Main_Page)) but we will see
