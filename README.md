# Common Slot

Find the time windows when everyone is available. Each participant supplies a list of ISO 8601 start and end pairs with UTC offsets. The output lists the full shared windows that meet the requested minimum duration, in UTC.

```sh
python common_slot.py example.json --minutes 30
```

Use Python 3.11 or later. See [example.json](example.json) for input from participants in two time zones. The tool uses only the Python standard library.

Run tests from the project directory with `python -m unittest -v`.
