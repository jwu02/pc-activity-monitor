## Commands
- `pipenv shell` to launch virtual environment
- `exit` to deactivate

## TODOs
- [] log messages with signals and add more log messages
- [] persist settings data locally
    - timeout interval
    - go online/offline on startup
    - offline data that needs syncing
- [] automatic configuration for development/production environment settings
    - python command options
    - shorter timeout intervals for testing
- [] track application time + activity grouping e.g. productivity, entertainment, gaming

- [x] reworked key press count implementation (holding down movements keys while gaming heavily inflates the count)
- [x] store+sync offline mode data / data that failed to send
- [x] fix pipenv installation
    - `imp` removed from python3.12 `https://github.com/BradenM/micropy-cli/issues/575`
    - `pip install pipenv --user`
    - `pipenv install --python 3.10`
- [x] rework online status widget
    - if toggling status to online, GET /ping to get response from API backend
- [x] add session data summary to dashboard