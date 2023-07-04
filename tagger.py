from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PasswordHashInvalidError, SessionPasswordNeededError

api_filename = 'api_info.txt'
api_id = ''
api_hash = ''
try:
    api_file = open(api_filename, 'r')
    info = api_file.readlines()
    api_id = info[0].strip()
    api_hash = info[1].strip()
    api_file.close()
except (FileNotFoundError, IndexError):
    api_file = open(api_filename, 'x')
    api_id = input("Enter api_id: ")
    api_hash = input("Enter api_hash: ")
    api_file.writelines([api_id, '\n',api_hash])
    api_file.close()

client = TelegramClient('me', api_id, api_hash)

if not client.is_connected():
    client.connect()   


def Login():       
    phone = input("Enter the phone number: ")
    client.send_code_request(phone)
    value = input("Enter the code from Telegram(if it hasn't arrived, restart the application after a few seconds): ")
    try:
        me = client.sign_in(phone, code=value)
    except SessionPasswordNeededError:
        while True:
            password = input("Enter the password: ")
            try:
                me = client.sign_in(password=password)
                break
            except PasswordHashInvalidError:
                print("Incorrect password! Try again!")

if not client.is_user_authorized():
    Login()

dialogs = client.get_dialogs()
dialogs = dialogs[-1 : -len(dialogs) - 1 : -1]

for i, dialog in enumerate(dialogs):
    print(f'{i}. {dialog.name}')   

chat_ids = []
chat_maxTagCount = []
messages = []

while True:    
    try:
        idx = (int)(input('Enter the chat index from the list(Type "-1" if you are ready to send the messages or "-2" to start anew): ')) 
        dialogs[idx]         
    except ValueError:
        print('Enter integer value (221, 15 and etc.)')
        continue
    except IndexError:
        print("No chat with such index was found!")
        continue  

    if idx == -1:        
        break
    elif idx == -2:
        chat_ids = []
        messages = []
        chat_maxTagCount = []
        continue
    print(f'You\'ve chosen  "{dialogs[idx].name}"')       

    all_part =  client.get_participants(dialogs[idx], aggressive= True)
    all_part = [part for part in all_part]
    i = 1
    for part in all_part:
        print(i, part.first_name, part.last_name, part.id, part.username)
        i += 1

    chat_ids.append(dialogs[idx].id)
    
    while True:
        try:
            maxTagCountInOneMsg = 0
            while maxTagCountInOneMsg <= 0 or maxTagCountInOneMsg > 10:
                maxTagCountInOneMsg = (int)(input('Enter the maximum amount of participants that will be tagged in one message(no more than 10): '))
            chat_maxTagCount.append(maxTagCountInOneMsg)
            break
        except ValueError:
            print("Enter the amount again!(1, 5, 10 and etc.)")

    isMessageCorrect = False
    while not isMessageCorrect:
        message = input("Enter your message and add 3 underscores where the tag-bom will be located(for example, 'Test___ message.'): ")
        if '___' not in message:
            print('You forgot to add underscores!')
            continue
        elif message[:3] == '___' and len(message) == 3:
            print("The message cannot consist only of underscores, try again! (например, 'Test___ message.')")
            continue
        messages.append(message)
        isMessageCorrect = True
        

for i in range(len(chat_ids)):    
    id = chat_ids[i]
    all_part =  client.get_participants(id, aggressive= True)    
    message = messages[i]    
    splitMessage = message.split('___')
    count = 0
    payload = ''

    maxTagCountInOneMsg = chat_maxTagCount[i]
    for partic in all_part:       
        count += 1 
        payload += f'<a href="tg://user?id={partic.id}">​</a>'        
        if count % maxTagCountInOneMsg == 0 and count != 0:              
            client.send_message(client.get_entity(id), '.' + payload, parse_mode= 'Html')
            payload = ''
    message = splitMessage[0] + payload + splitMessage[1]    
    client.send_message(client.get_entity(id), message, parse_mode= 'Html')

input("Done! Press Enter to exit...")
client.disconnect()