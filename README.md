# roboronya
Hangouts bot just for fun.

## Description

`roboronya` uses [hangups](https://github.com/tdryer/hangups) to connect to a Google gmail account and listens to the
incoming chats of that account to look for [implemented commands](https://github.com/synnick/roboronya/blob/master/commands.py#L15).

A `requirements.txt` file is included with the dependencies that `roboronya` requires.

In order for `roboronya` to work, these environment variables must be set:
- `ROBORONYA_EMAIL`: Plain Gmail account email.
- `ROBORONYA_PASSWORD`: Plain Gmail account password.

**Note: These are not used for any malign purpose for `roboronya`, they are just used to connect to hangouts
via `hangups`.**

To execute the `roboronya` bot just run:
```
python3 roboronya.py
```

## TODO
- Implement `/gif` command.
- Better Exception handling and logging.
- Make command API more robust without sacrificing simplicity.
- Add a more reliable way for looking up commands in message.
