# roboronya [![Build Status](https://travis-ci.org/synnick/roboronya.svg?branch=master)](https://travis-ci.org/synnick/roboronya)
Hangouts bot just for fun.

## Description

`roboronya` uses [hangups](https://github.com/tdryer/hangups) to connect to a Google Gmail account and listens to the
incoming chats of that account to look for [implemented commands](https://github.com/synnick/roboronya/blob/master/commands.py#L13).

## Installation

Installation is fairly simple for those familiar with Python. A `requirements.txt` file is included with the dependencies that `roboronya` uses. Since `hangups` uses `Python3`, this project is implemented in `Python3` as well, currently using the `3.3.6` version. Other than that, the only extra requirement is a Google Gmail account, whose credentials `hangups` will prompt for when running `roboronya` for a first time (or when the refresh token expires).

**Please Note: These are not used for any malign purpose for `roboronya`, they are just used to connect to hangouts
via `hangups`.**

To execute the `roboronya` bot just run:
```
python3 roboronya.py
```

After a correct login, `roboronya` will connect and listen to incoming events, currently only processing `hangups.ChatMessageEvent`. Each chat event message is parsed to look for slash commands, i. e.
```
/gif cute corgi
```

For any given command, the following words (until before the next command) are parsed and provided to the command "interfaces" (which are plain Python functions for which a `/{command_name}` is redirected.

[To create a new command a simple function is required!](https://github.com/synnick/roboronya/blob/master/commands.py#L253).

## TODO
- More fun commands.
- Make command API more robust without sacrificing simplicity. Also Web API would be nice so other languages can interact.
- Better Exception handling and logging.
- Add a more reliable way for looking up commands in message.
- Tests (eventually... maybe...).
