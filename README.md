# MeleeRecoveryBot
SmashBot that helps the player in practicing edgeguarding. Based on the work of AltF4's **[Smashbot](https://github.com/altf4/SmashBot)**.

# Currently Supported Characters/Stages
**Player Characters**: Captain Falcon, Falco, Fox, Ganondorf, Jigglypuff, Marth, Peach, Pikachu, Samus, Sheik, Zelda<br>
(NOTE: you can choose other characters, but the bot will not DI properly for throws)<br>
<br>
**Smashbot Characters**: Captain Falcon, Fox, Falco, Ganondorf<br>
<br>
**Stages**: Battlefield, Dreamland N64, Final Destination, Fountain of Dreams, Pokemon Stadium (frozen), Yoshi's Story<br>
(NOTE: recoveries involving platforms are not yet supported, and the bot has only been extensively tested on Final Destination so far)

# How to get Started
1. ~~**The bot only functions correctly with Slippi up to version 2.3.1**, so if you do not have that version of Slippi installed, you need to install it separately.~~ The bot now works on all versions of Slippi.
2. Clone this repository to somewhere on your computer (ideally, a place where you do not need to elevate your permissions to access, such as your Documents folder).
3. Follow the setup steps found on AltF4's Smashbot, including the part where you run the SmashBot executable.
4. When the game starts, navigate to the Character Select Screen. The bot will select a character.
5. It's recommended that you change the settings of the match if you plan to practice edgeguarding for an extended time.
6. Pick a supported stage to get started.

# Difficulty Settings
The SmashBot has a few preset difficulty settings that change how it will recover back onto stage. You can change the difficulty when running the <code>smashbot.py</code> command with the <code>-i</code> argument.
## Difficulty 0: Beginner
- One recovery option is chosen (usually Up Special)
- Recovery always starts as high as possible
- Recovery aims to go as far in stage as possible
- Always hold in on drift
- Never grab ledge, even if reachable
- Trajectory DI is always neutral
- Smash DI is zero
- Fast-falling is never performed
- Amsah teching is never performed
- Ledge teching is never performed
- No extra recovery tactics are performed
- Meteor canceling is not performed
## Difficulty 1: Easy
- Two recovery options are chosen (usually Side Special, and Up Special if first option cannot make it)
- Recovery can start as high as possible or low enough to get to ledge
- Recovery always aims to ledge if possible
- Always hold in on drift
- Never grab ledge, even if reachable
- Trajectory DI is away when hit towards stage, otherwise for survival
- Smash DI is zero
- Fast-falling is never performed
- Amsah teching is never performed
- Ledge teching is never performed
- Simple extra recovery tactics are performed regardless of safety (e.g. Falcon Kick)
- Meteor canceling is performed very slowly
## Difficulty 2: Normal
- Three recovery options are chosen evenly (usually Side Special, Air Dodge, and Up Special if neither previous option can make it)
- Recovery can start anywhere
- Recovery can aim anywhere, excluding downward angles to ledge
- There is some chance to do an early fade-back drift
- Always grab ledge if reachable
- Trajectory DI is away when hit towards stage or hit weakly off stage, otherwise for survival
- Smash DI is slight
- Fast-falling is always performed
- Amsah teching is always performed, even when unsafe to do so
- Ledge teching is performed some of the time if possible
- Simple extra recovery tactics are performed more safely
- Meteor canceling is performed slowly
## Difficulty 3: Hard
- Three recovery options are chosen (usually Side Special, Up Special, and Air Dodge)
- Recovery can start anywhere
- Recovery can aim anywhere, including downward angles to ledge
- Even chance between fading back early, fading back late, and holding in for drift
- Equal chance to grab ledge or use move when ledge is reachable
- Trajectory DI is away when hit towards stage or hit a bit more strongly off stage, otherwise for survival
- Smash DI is high (for a human)
- Fast-falling is always performed
- Amsah teching is performed only when safe to do so, and slide-offs are preferred if it will send the bot to the ledge
- Ledge teching is always performed if possible
- More complicated extra recovery tactics are occasionally performed, and safely
- Meteor canceling is performed perfectly
## Difficulty 4: TAS
- Three recovery options are chosen (Up Special most common, occaisionally chooses options like Side Special or Air Dodge)
- Recovery can start anywhere
- Recovery can aim anywhere, including downward angles to ledge
- Even chance between fading back early, fading back late, and not fading back at all
- Equal chance to grab ledge or use move when ledge is reachable
- Trajectory DI is away when hit towards stage or hit a bit more strongly off stage, otherwise for survival
- Smash DI is frame-perfect
- Fast-falling is always performed
- Amsah teching is performed only when safe to do so, and slide-offs are preferred if it will send the bot to the ledge
- Ledge teching is always performed if possible (extra Smash DI makes them far more frequent)
- More complicated extra recovery tactics are always performed, and safely
- Meteor canceling is performed perfectly

# Limitations & Problems
- **The bot only functions correctly with Slippi up to version 2.3.1**
- The bot will frequently bug out the Character Select Screen when you go to change the game options. The workaround is to not go into those settings more than once
- The bot will not adjust recovery based on any action the player is doing (apart from hit mitigation such as DI'ing and teching)
- The bot will not recover to side or top platforms
- The bot will occasionally SD or perform an obviously wrong option as a result of many of its actions needing to be frame-perfect

# Eventual Goals
- Support for recovering to platforms on stages (probably not Randall on Yoshi's Story anytime soon)
- Support for more SmashBot characters
- Support for more player characters
- Adapt recovery based on player state
- Adapt recovery tactics based on previous successful/failed player edgeguards
- Make a build for UnclePunch's **[Training Mode](https://github.com/UnclePunch/Training-Mode)** to adjust specific settings in-game
