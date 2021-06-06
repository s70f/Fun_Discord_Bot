# About The Project
(name) is a Discord Bot developed with Discord.py, it has fun games and commands that will lighten up your server.

## Setup and Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Discord.py.

```bash
pip install discord.py
```
Ensure that the words.txt and Cogs folder is in the same directory as main.py

## Commands
Here is a list of commands the bot has built in.

### Command Prefix
The command prefix is "." and can be changed with the `.prefix <prefix>` command.

### Word Scramble
The `.unscramble` command gives you a scrambled word to unscramble (good luck).

### Odds Generator
The `.odds <lowest number> <highest number>` lets you pick a number within the range you specified. If the number matches the number the bot chose you're in big trouble because you'll be muted for that many minutes.

### Mine
The Mine is a fun economy system that allows you to mine for gems in the deep dark. Upgrade mining capabilities, boost your collection rate and sell gems for a high price. 

### Gems
There are three types of Gems you can find; Opals which have the most value and can only be found in the darkest caverns. Emeralds can be found in chunks of 3-4 and have the second-highest value. Rubies can be mined extremely fast with the right equipment and can be found in any cave. 

### Gold
Gold can be obtained by winning duels or exchanging gems for it.

### Market
The market is where all the buying and selling happens. keep in mind prices for gems change every 3 hours so be on the watch for amazing deals. Players can sell their items for any price they want to other players or sell them to the market for the base price.

### War
Players can use start a battle against any player with the `.war @mention` command. Players start off with a random number of soldiers ranging from 30 - 40 *note: range can vary depending on the class. Players can choose their method of attack, normal attack, catapults, specialty, rage attack; or can choose to reinforce their army by having a rescue mission, recruiting soldiers from the catapults, or train new ones. Different classes have different perks and drawbacks. 

### Classes
Players can choose between 4 classes before they start a battle by using `.class <type>`

#### Sniper
An elite killing squad. Increases the maximum amount of damage you can deal by 1 but decrease the minimum amount of soldiers you start with by 5.

#### Marksmen
A band of ruthless soldiers who spray at any living thing. Decreases the maximum amount of damage you can deal by 1 but increases the minimum amount of soldiers you start with by 5.


#### Infantry
The infantry is specialized in combat on foot. This guarantees you, +5 soldiers, to start off with but doesn't allow you to enable cavalry or use rage commands.

#### Artillery
Artillery is a class of heavy military ranged weapons built to launch munitions far beyond the range and power of infantry firearms. You start off with -6 soldiers but get 1 extra ammo and catapults from enemy deals -1 damage.
