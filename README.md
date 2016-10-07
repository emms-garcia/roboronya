# roboronya
Hangouts bot just for fun.

## Description

`roboronya` uses [hangups](https://github.com/tdryer/hangups) to connect to a Google Gmail account and listens to the
incoming chats of that account to look for [implemented commands](https://github.com/synnick/roboronya/blob/master/commands.py#L18).

A `requirements.txt` file is included with the dependencies that `roboronya` requires. Since `hangups` uses `Python3`, this project is implemented in `Python3` as well.

In order for `roboronya` to work, these environment variables must be set:
- `ROBORONYA_EMAIL`: Plain Gmail account email.
- `ROBORONYA_PASSWORD`: Plain Gmail account password.

**Please Note: These are not used for any malign purpose for `roboronya`, they are just used to connect to hangouts
via `hangups`.**

To execute the `roboronya` bot just run:
```
python3 roboronya.py
```

## TODO
- Make command API more robust without sacrificing simplicity. Also Web API would be nice.
- Better Exception handling and logging.
- Add a more reliable way for looking up commands in message.
- Tests (eventually... maybe...).
