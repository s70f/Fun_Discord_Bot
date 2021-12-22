# About The Project (BETA)
(name) is a Discord Bot developed with Discord.py, it has fun games and commands that will lighten up your server.

## Setup and Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Discord.py.

```bash
pip install discord.py
```
Ensure that the words.txt and Cogs folder is in the same directory as main.py

## Commands
Here is a list of commands the bot has built-in.

### Command Prefix
The command prefix is "." and can be changed with the `.prefix <prefix>` command.

### Word Scramble
The `.unscramble` command gives you a scrambled word to unscramble (good luck).

### Odds Generator
The `.odds <lowest number> <highest number>` lets you pick a number within the range you specified. If the number matches the number the bot chose you're in big trouble because you'll be muted for that many minutes.

## War
Players can use start a battle against any player with the `.war @mention` command. Players start off with a random number of soldiers with a range depending on the class (read more about classes later). Different classes have different perks and drawbacks. Players can choose their method of attack (read more about attacks later).

### Attack
There are 4 types of attacks. You will want to choose your attacks wisely based on the market price and your economy.

#### Light Attack
The default attack, `.attack light` does 2-5 damage and costs 3-10 credits

#### Heavy Attack
`.attack heavy` does 6-9 damage and costs 15-30 credits

#### Catapult
`.attack catapult` does 10 damage and costs 30-50 credits

#### Assassin
`.attack assassin <number of assassins>` does 1 damage multiplied by the number of assassins and costs 6 - 14 credits multiplied by the number of assassins. 

#### Catapult
`.attack surprise` generates 4 random coordinates (unique numbers from 0-10) and the opponent has to guess them. 4 damage for each coordinate guessed wrong and the enemy gets 10 credits per guessed coordinate. 

#### More
`.attack poison` coming soon

### Market
The `.market` is where players can look at the price of attacks. Each turn, the market changes price. Make sure to choose wisely.

### Gold
Gold can be obtained by winning duels. To calculate the amount of gold you get per win just take the number of soldiers you have left and add 10 to that. 

### Classes
There are 4 main classes a player can choose from before they start a battle using `.main class <type>`. Players can also unlock classes by buying or getting achievements. Use `.market class` to see different classes available for purchase. Use `.main classes` to see all the classes you are able to choose from.

#### Sniper
An elite killing squad. Increases the maximum amount of damage you can deal by 1 but decrease the minimum amount of soldiers you start with by 5.

#### Marksmen
A band of ruthless soldiers who spray at any living thing. Decreases the maximum amount of damage you can deal by 1 but increases the minimum amount of soldiers you start with by 5.


#### Infantry
The infantry is specialized in combat on foot. This guarantees you, +5 soldiers, to start off with but doesn't allow you to enable cavalry or use rage commands.

#### Artillery
Artillery is a class of heavy military ranged weapons built to launch munitions far beyond the range and power of infantry firearms. You start off with -6 soldiers but get 1 extra ammo and catapults from enemy deals -1 damage.

## Next Phase
Make a credit system where you have to buy different types of soldiers and save credits and get credits for winning

