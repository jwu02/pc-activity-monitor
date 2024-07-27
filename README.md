## Commands
- `python -m env` create virtual environment
- `source env/Scripts/activate` activate environment
- `deactivate` deactivate
- `pip freeze > requirements.txt` create requirements file
- `pip install -r requirements.txt` install dependencies

## TODOs
- [] log messages with signals and add more log messages
- [] persist settings data locally
    - selected timeout interval
    - launch app on pc startup
    - go online/offline on app startup
    - unsynced data
- [] automatic configuration for development/production environment settings
    - python command options
    - use shorter timeout intervals for testing
- [] track other desktop app time + activity grouping e.g. productivity, entertainment, gaming

- [x] changed key press count implementation
    - holding down movements keys while gaming heavily inflates the count
    - don't count key unless it was previously released/lifted after pressing down
- [x] store+sync offline mode data / data that failed to send
- [x] fix pipenv installation (not using pipenv anymore)
    - `imp` removed from python3.12 `https://github.com/BradenM/micropy-cli/issues/575`
    - `pip install pipenv --user`
    - `pipenv install --python 3.10`
- [x] rework online status widget
    - if toggling status to online, GET /ping to get response from API backend
- [x] add session data summary to dashboard