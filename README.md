# mac-stock-menu-bar
python3 needs to be installed.
```
python3 -m venv venv
source venv/bin/Actiavate
pip install -r requirements.txt
python main.py
```
## troubleshooting
### No module named '_tkinter'
```
import _tkinter # If this fails your Python may not be configured for Tk
    ^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named '_tkinter'
```
MacOS originally has tkinter and python inside its system, but it has very complicated version problem. Hence I recommend to use `brew` or `pyenv` installed python and tkinter.
```
brew install python
brew install python-tk
```
would fix your problem.

If this problem continues you can use backup.py instead of main.py but nah rumps UI sucks


### export py2app