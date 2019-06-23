# OpenCV based Overwatch Aimbot
This project was a 24 hour deep dive experiment into image processing
and applying what I learned into something practical.
> If support gains around it, I will continue the weekend experiment

**THIS IS FOR EDUCATIONAL
PURPOSES ONLY AND SHOULD NOT BE USED IN-GAME AT RISK OF ACCOUNT SUSPENSION**

<img src="doc/media/prototype.gif" width="400">

### What is it?
This experiment uses [OpenCV](https://opencv.org/)'s python library to extract
characters in real-time out of the popular game Overwatch.  It then uses Windows
API events to simulate mouse movements and automatically aim at a nearby enemy
player.

## Configuration
Check the version in `.python-version` for the least friction in using the
required libraries or if you have `pyenv` simply run
```bash
pyenv install
```
in the root directory of the project.

#### Dependencies
To install the required dependencies using pip, use
```bash
pip install -r requirements.txt
```

Note that pywin32 may need the `postinstall` script ran
```bash
python Scripts\pywin32_postinstall.py -install
``` 
from an **elevated command prompt** where your pip dependencies are installed.

#### Limitations
Current limitations include:
- Overwatch client must be centered in the
desired monitor **or** in Fullscreen/Windowed Fullscreen mode.
- The enemies must be in **MAGENTA**
  - You can toggle this setting in the Overwatch client's color blind settings
- The targeting system needs a bunch of tweaking that I just didn't get around to
in the set amount of time I took to make the prototype.
- The aimbot may be identifiable by internal cheat prevention systems, there should
be some work done on the targeting system and amount of messages sent to the windows
API
- There are no unit tests, so there's truly no objective way to benchmark the
improvement of a change

#### Running
You can run the aimbot with
```bash
python -o ow.py
```
And also run it with a visual output by omitting the `-o` flag
```bash
# Run in debug mode
python ow.py
```

Targets will only be targeted if they're within the defined `MAX_TARGET_DISTANCE`
and the `Caps Lock` key is held down

---
Big thanks to my friend [@EatonChips](https://github.com/eatonchips) for helping
me tweak the HSV value ranges

#### Want to support the Project?
Feel free to make a new branch and open a PR!  Also, I am permabanned
and would love an alternate account if you have spare <3
