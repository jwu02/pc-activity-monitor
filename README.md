## Commands
- `pipenv shell` to launch virtual environment
- `exit` to deactivate

## TODOs
- store+sync offline mode data / data that failed to send
- persist settings data locally
    - timeout interval
    - go online/offline on startup
    - offline data that needs syncing
- automatic configuration for development/production environment settings
    - python command options
    - shorter timeout intervals for testing
- track application time + activity grouping e.g. productivity, entertainment, gaming
- fix pipenv installation

- [x] rework online status widget
    - if toggling status to online, GET /ping to get response from API backend
- [x] add session data summary to dashboard