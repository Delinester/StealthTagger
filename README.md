# Telegram Stealth Tagger

This is a simple script that allows you to tag all members of a small group being unrecognized doing this! 

## Limitations

The script **WON'T** work in groups that have more than 2000 members (> 2000).
The script is mostly suitable for groups with **small** number of participants (less than 100) because for every 10th member there is one message with tags

### Prerequisites

You should have *Telethon* library installed in order to use the script

```
pip install telethon
```

## First use

1. Run the script
2. Go to https://my.telegram.org/ , log in there and create application.
3. Copy '**api_id**' and paste it into the script console
4. Copy '**api_hash**' and paste it into the script console
5. Log in into telegram (enter phone, code, password)
6. You will be given all chats that you have in your telegram account. Now you need to choose the one where you want to send a message with tag-bomb (indices are on the left)
7. Enter the amount of participants that will be tagged in one message.
If the whole amount of participants exceeds group member count, messages with dot('.') will be send consequently
```
.
.
.
My message___
```
8. Enter the message itself and add 3 underscores where to place invisible tags
9. If you want, you can add more chats to send messages to(separate message to each one) or begin the process by typing '-1'

## How to change the account?

Just delete '*api_info.txt*' to change API info
Delete '*.session*' file to change telegram account

## License

This project is licensed under the MIT License 
