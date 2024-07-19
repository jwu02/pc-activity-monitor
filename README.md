# TODOs
- handle cases where data may fail to send e.g. due to no internet connection
    - rework online_status_label to get a response from the API
- store+sync offline mode data / data that failed to send
- persist settings data locally
    - timeout interval
    - go online/offline on startup
    - offline data that needs syncing
- automatic configuration for development/production environment settings
    - python command options
    - shorter timeout intervals for testing
- track application time + activity grouping e.g. productivity, entertainment, gaming

- [x] add session data summary to dashboard