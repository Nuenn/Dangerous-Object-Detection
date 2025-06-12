##

### Installation

#### Pre-requisite
- It advisable to use `Anaconda` for creating a separate `Python` environment, you can download it [here](https://www.anaconda.com/download/).
---
#### Step 1 - Install package
1. `pip install ultralytics`
2. `pip install python-telegram-bot --upgrade`
3. `pip install aiogram`
> Install the package using terminal/cmd or powershell
![terminal](readme/1.png)

---

#### Step 2 : Create telegram Bot
1. Open telegram and search `BotFather`.
> ![terminal](readme/2.png)
2. Send `/start` in the chat.
3. Send `/newbot` in the chat.
4. Send your bot name ex. `Bomoh`.
5. Send username for the bot ex. `myusername`.
6. You will receive the APi token for your bot.
> ![botApi](readme/3.png)
7. open `prototype.py` and change APiToken value to your BOT APi token.
> ![botApi](readme/4.png)

---

#### Step 3 - Run
1. Download the .zip that contain the script for object detection.
2. Copy to any directory.
3. Extract the zip file.
4. Open the `terminal`/`cmd` or `powershell` and navigate to the destination using `cd` example: `cd C:\Users\faryz\Documents\Python Project\YOLO object detection`
5. run `python prototype.py` inside the `terminal`/`cmd` or `powershell
> Example

![run gif](readme/run-script.gif)
