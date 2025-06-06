# Ninja Fight (Game)

Naruto vs Sasuke Game
Overview
This is a 2D action game built with Python and Pygame, featuring a battle between Naruto and Sasuke from the popular anime series. Players control Naruto, navigating a platform-style environment, throwing shurikens, and collecting health potions to defeat Sasuke across multiple levels. The game includes animated sprites, background music, sound effects, and a progressive level system with saved progress.
Features

Gameplay:
Control Naruto to move left/right, jump, and throw shurikens.
Battle Sasuke, who moves automatically and throws shurikens in higher levels.
Collect health potions to restore Naruto's health (available from level 3).


Levels:
Multiple levels with increasing difficulty (Sasuke's speed and shuriken frequency increase).
Progress is saved to a progress.txt file, allowing players to resume at the highest unlocked level.


Graphics and Audio:
Animated sprites for Naruto and Sasuke (walking, standing, and death states).
Background images and a static GIF-like animation for the start screen.
Background music (naruto_mix.mp3) and hit sound effects (hit.wav).
Toggle sound on/off via the pause menu.


User Interface:
Start screen with a "START" button.
Level selection screen with unlocked levels highlighted.
Pause menu with options to continue, retry, toggle sound, or exit.
Win/lose screens with retry and return options.
Health bars for both characters and a level indicator.


Mechanics:
Collision detection for shurikens, health potions, and character interactions.
Naruto wins by depleting Sasuke's health; Sasuke wins by depleting Naruto's.
Randomized background changes per level and health potion spawns.



Prerequisites

Python 3.6+
Pygame (pygame27` for graphics and audio
Required Python packages:
pygame


Assets (included in the pics directory):
Sprite images (*.png): Naruto and Sasuke animations, backgrounds, shuriken, health potion, etc.
Audio files: naruto_mix.mp3 (background music), hit.wav (sound effect).
Static GIF-like background (front 2.jpg).



Installation

Clone the Repository:git clone <repository-url>
cd naruto-vs-sasuke


Install Dependencies:pip install pygame


Ensure Assets:
Place all required image and audio files in a pics subdirectory within the project folder.


Run the Game:python naruto_vs_sasuke.py



Usage

Start Screen: Click the "START" button to proceed to the level selection screen.
Level Selection: Choose an unlocked level (1 to 8, based on saved progress) or select "Restart Game" to reset to level 1.
Controls:
Left Arrow: Move Naruto left.
Right Arrow: Move Naruto right.
Up Arrow: Make Naruto jump.
Spacebar: Throw shuriken (up to 5 at a time).
P Key: Pause/unpause the game.


Pause Menu:
Options: Continue, Retry Level, Toggle Sound (On/Off), Exit.


Gameplay:
Deplete Sasuke's health to win and advance to the next level.
Avoid Sasuke's shurikens and collisions, which reduce Naruto's health.
Collect health potions (levels 3+) to restore 20 health points.


Win/Lose:
Win: Naruto depletes Sasuke's health, advances to the next level, and saves progress.
Lose: Sasuke depletes Naruto's health, offering options to retry the level or return to the start screen.



Directory Structure
naruto-vs-sasuke/
├── pics/                   # Directory containing game assets
│   ├── NR1.png, NR2.png, NR3.png  # Naruto right-facing sprites
│   ├── NL1.png, NL2.png, NL3.png  # Naruto left-facing sprites
│   ├── SR1.png, SR2.png, SR3.png  # Sasuke right-facing sprites
│   ├── SL1.png, SL2.png, SL3.png  # Sasuke left-facing sprites
│   ├── Nh.png, Sh.png            # Naruto and Sasuke health bar icons
│   ├── Nd.png, Sd.png            # Naruto and Sasuke death sprites
│   ├── shur.png                  # Shuriken sprite
│   ├── health_potion.png         # Health potion sprite
│   ├── bg1.png, bg2.png, bg3.png, bg4.png  # Background images
│   ├── front 2.jpg               # Start screen background
│   ├── naruto_mix.mp3            # Background music
│   ├── hit.wav                   # Hit sound effect
├── progress.txt            # File to store highest unlocked level
├── naruto_vs_sasuke.py     # Main game script
├── README.md               # This file

Notes

Asset Requirements: Ensure all images and audio files are present in the pics directory. Missing assets will trigger error messages and fallback to a default surface or silence.
File I/O: The game saves progress to progress.txt in the project directory. Ensure write permissions are available.
Performance: The game runs at 25 FPS to balance animation smoothness and performance.
Sound: Background music loops continuously; sound effects play on hits. Sound can be toggled in the pause menu.
Error Handling: The game includes basic error handling for missing files, with fallbacks to prevent crashes.
Future Improvements:
Add a draw condition (e.g., both characters survive for a set time).
Implement a main menu with settings (e.g., volume control).
Add more levels or enemy behaviors.
Support for additional characters or power-ups.



License
This project is licensed under the MIT License. See the LICENSE file for details.
Contributing
Contributions are welcome! Please submit a pull request or open an issue for bug reports, feature requests, or improvements.
Acknowledgments

Inspired by the Naruto anime series.
Built with Pygame, a powerful library for 2D game development in Python.

