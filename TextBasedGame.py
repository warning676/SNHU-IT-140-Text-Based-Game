# Benjamin David Reynolds

import time # For delays

# DEBUG VARIABLES
start_with_powers = False # To start with supernatural powers every time, set this to True

def show_instructions(inventory):
    """
    Displays information and list of commands available to the player.
    - inventory: contains items that player collects
    Returns a string containing the article
    """
    print('INFORMATION:')
    print('-' * 24)
    print("In search of a missing person, you play as a detective looking for clues, "
          "but be aware, there's a danger lurking around...\n"
          "Find weapons to defend yourself, or even find clues.\n"
          "You can either collect the 6 necessary items to win the game, "
          "or you can suffer the consequences of not doing so.\n"
          'There’s a secret concealed within these walls, invisible to the "rooms" command. '
          "Only those who search carefully will uncover it and unlock new abilities.\n")
    print('COMMANDS:')
    print('-' * 24)
    print('Move commands consist of: "go"/"move"/"travel" north south east or west.\n'
          'Inventory commands consist of: "get"/"grab"/"take" item name.\n'
          'Extra commands consist of: "exit"/"quit" to quit the game, "help"/"info"/"commands" to show commands, '
          'and "rooms" to show all rooms.\n')
    if 'Supernatural Powers' in inventory:
        print('Now that you have found Supernatural Powers, you can use your powers by typing "powers".')
    return None

def powers(inventory, current_room, rooms):
    """
    Powers menu that takes action based on user input.
    - inventory: contains items that player collects
    - current_room: player's current room
    - rooms: dictionary of room connections
    Returns an updated current_room
    """
    while True:
        print('POWERS MENU:')
        print('-' * 24)
        print('1. Add all items to inventory.'
            '\n2. Teleport to any room.'
            '\n3. Exit Menu')
        print('-' * 24)
        user_input = input('Type a number (1-3): ').strip() # User prompted to select number in valid range
        # If user inputs "1", notify player all items will be deleted from rooms, and add every item to inventory
        if user_input == '1':
            user_input = input('\nThis will also delete every item from all rooms.\n'
                            'Do you want to continue? (Y or N): ').upper().strip()
            print()
            if user_input == 'Y' and len(inventory) < 7:
                for room in rooms.values():
                    # Check if there is an item in each room, and verify "Villain" is not one of those items
                    if 'Item' in room and room['Item'] != 'Villain':
                        item = room['Item']
                        print(f'Item added to inventory: {item}')
                        inventory.append(item)
                        del room['Item']
                inventory.sort() # Sort inventory to retain alphabetical order
                print()
            elif user_input == 'N':
                pass
            else:
                print('You already have every item.\n')
        # If player input is "2", then show rooms, prompt user to input room and teleport to desired room
        elif user_input == '2':
            print('ROOMS AVAILABLE TO TELEPORT TO:')
            print('-' * 24)
            show_rooms(current_room, rooms) # Display all rooms
            print('-' * 24)
            user_input = input('Type a room to teleport to (or N to cancel): ').title().strip()
            print('-' * 24)
            if user_input == current_room:
                print('You are already in this room.')
            elif user_input in rooms.keys():
                current_room = user_input
                print(f'You teleported to the {current_room}.')
            elif user_input == 'N':
                pass
            else:
                print(f'{user_input} is not a valid room.')
        elif user_input == '3':
            break
        else:
            print(f'\n"{user_input}" is not a valid number between 1-3.\n')

    return current_room

def show_rooms(current_room, rooms, status=False):
    """
    Shows all rooms to player and notifies them of connected rooms.
    - item_name: name of the requested item
    Returns nothing
    """
    for room in rooms.keys():
        # Hide the Secret Room unless the player has entered it
        if room == 'Secret Room' and rooms[room]['Player Entered'] == False:
            continue

        marker = '← You are in this room.' if room == current_room else ''
        status_text = ' (Explored)' if status and rooms[room]['Player Entered'] else ' (Unexplored)'
        dir_text = ''

        directions = []
        for direction, connected_room in rooms[current_room].items():
            # Find which directions connect the current room to this one
            if direction in ['North', 'South', 'East', 'West'] and connected_room == room:
                directions.append(direction)
            dir_text = f'↳ This room is {', '.join(directions)} from the {current_room}.' if directions else ''

        print(f'{room:<20}{status_text:<12} {marker}')
        if dir_text:
            print(f'    {dir_text}')

    return None

def get_article(item_name):
    """
    Determines which article to use based on the five main vowels.
    - item_name: name of the requested item
    Returns a string containing the article
    """
    no_article = {'body armor', 'supernatural powers'} # These items should not use articles
    if item_name.lower() in no_article:
        return None
    elif item_name[0].lower() in 'aeiou':
        return 'an'
    else:
        return 'a'

def display_information(current_room, rooms, dialogue, inventory):
    """
    Display's status of current room, inventory, and dialogue.
    - current_room: player's current room
    - rooms: dictionary of room connections
    - dialogue: dictionary of every dialogue
    - inventory: contains items that player collects
    Returns nothing
    """
    print('-' * 24)
    print(f'You are in the {current_room}.') # Display status of player's current room
    # Display status of player's inventory in a clean manner
    print(f'You have {len(inventory)} {'items' if len(inventory) > 1 else 'item' } in your inventory: '
          f'{', '.join(inventory)}' if inventory else
          'You have no items in your inventory yet.\nExplore different rooms to find items.')
    # If player has entered their current room before, skip over dialogue else print dialogue
    if rooms[current_room]['Player Entered']:
        pass
    else:
        print(dialogue[current_room])
        rooms[current_room]['Player Entered'] = True
    # If there is an item in the players current room, then print the item
    if 'Item' in rooms[current_room]:
        current_room_item = rooms[current_room]['Item']
        article = get_article(current_room_item) # Determine which article to use based on the item
        if article is None:
            print(f'\nYou see {current_room_item}.')
        else:
            print(f'\nYou see {article} {current_room_item}.')
    return None

def check_status(current_room, inventory):
    """
    Checks the player's current status to determine certain actions.
    - current_room: player's current room
    - rooms: dictionary of room connections
    - inventory: contains items that player collects
    Returns nothing
    """
    # Quit the game if player is in the 'exit' room
    if current_room == 'Exit':
        quit(0)
    # Once player has the Supernatural Powers item and code has not run before, then print
    elif 'Supernatural Powers' in inventory and not getattr(check_status, 'ran_once_1', False):
        print('-' * 24)
        print('Now that you have found the secret, you use certain abilities.\nType "powers" to show abilities.')
        check_status.ran_once_1 = True # Make sure this code does not run twice
    # Once player has collected all necessary items to defeat the villain, they are notified
    elif len(inventory) >= 6 and not getattr(check_status, 'ran_once_2', False):
        print('-' * 24)
        print('You now have the necessary items to defeat the villain.\n'
              'Conquer the villain by finding the room the villain is hiding in.')
        check_status.ran_once_2 = True
    # Check if player is in the dungeon
    elif current_room == 'Dungeon':
        has_powers = 'Supernatural Powers' in inventory # Does player have Supernatural Powers item?
        item_count = len(inventory) # Length of players inventory
        required_items = 7 if has_powers else 6 # Required items to win the game, changes if player has powers
        # If the player does not all necessary items end the game
        if item_count < required_items:
            print('-' * 24)
            print('You entered the room of the villain unprepared, and the villain ended you.')
            # Remaining items for player to collect in order to win
            remaining = 6 - len(inventory) if 'Supernatural Powers' not in inventory else 7 - len(inventory)
            # Remind the player to collect the necessary items if no items were collected, otherwise print remaining items
            print('Make sure to collect the necessary items to defeat the villain.'
                  if not inventory else f'You had {remaining} item{'s' if remaining != 1 else ''} left to collect.')
            time.sleep(5)
            quit(0)
        # Player has won, so print victory story
        else:
            print('-' * 24)

            print("You enter the room of the villain, "
                  "everything was quiet until you hear the dirty old floorboards creak behind you...")
            time.sleep(4)

            print("The villain sneakily attacks you with a heavy hit, "
                  "but your body armor along with your helmet deflect the damage that could have ended fatally.")
            time.sleep(5)

            print("You then pull out your flamethrower, using it in a savage manner and as you keep burning the villain, "
                  "it retreats further and further back and eventually loses sight of you.")
            time.sleep(4)

            print("You decide to throw a toothbrush to distract the villain, which luckily works in your favor.")
            time.sleep(2)

            print("Now, as the villain is distracted, to replenish your strength you quickly eat your apple, "
                  "and then your steak, which had been cooked by your flamethrower.")
            time.sleep(3)

            print("Now you are confident you have enough strength to defeat the villain once and for all.")
            time.sleep(2)

            print("The villain is visibly frustrated and in pain as it wanders around the dark lair, "
                  "and is tracking the scent of the toothbrush with its dog-like senses in search for you.")
            time.sleep(5)

            print("All is quiet again, you hear the faint sounds of sniffing, "
                  "but you then see a hand come from around the box you hid behind.")
            time.sleep(3)

            print("The villain launches an attack towards you, knocking the flamethrower out of your hand.")
            time.sleep(3)
            # Change story here if player has Supernatural Powers
            print("It all seems as if it is over, but the villain passes out shortly after." if 'Supernatural Powers'
                  not in inventory else 'As a last resort, '
                                        'you use your powers to propel the villain into outer space.')
            time.sleep(2)

            print("The villain ushers its last breath... and dies.")
            time.sleep(3)

            print("After defeating the villain, you notice a strange golden key on the ground, "
                  "so you pick it up along with your flamethrower.")
            time.sleep(3)

            print("You then hear distant crying, echoing throughout the entire dungeon, but who could it be?")
            time.sleep(3)

            print("You slowly but hesitantly approach the unsettling sound "
                  "as you look over your shoulder for lurking danger.")
            time.sleep(3)

            print("Straight ahead of you, in the distance, you see a jail cell and a figure resembling a person.")
            time.sleep(3)

            print("In a fearful manner, you walk up to the person while holding your flamethrower, "
                  "ready to act any second.")
            time.sleep(3)

            print("The person seems familiar, but you cannot trust them quite yet.")
            time.sleep(2)

            print("You ask a few questions to build rapport with the person and decide enough is enough "
                  "and let them free.")
            time.sleep(3)

            print("The jail cell is locked, but luckily the villain dropped that strange key from earlier, "
                  "you used the key to open the cell and walk out with the person.")
            time.sleep(3)

            print("\nYou won the game! Great job!")
            time.sleep(2)

            quit(0)

    return None

def evaluate_command(user_command, current_room, rooms, inventory, dialogue):
    """
    Processes the player's command and updates the current room if needed.
    - command: string input from player's command
    - current_room: player's current room
    - rooms: dictionary of room connections
    - inventory: contains items that player collects
    - dialogue: dictionary of every dialogue
    Returns the updated current_room
    """
    command = user_command.strip().lower().split() # Clean up and split input
    # Empty input, no change
    if not command:
        return current_room

    print('-' * 24)

    verb = command[0] # The first word the player typed
    args = command[1:] # Every word past the first word the player typed
    # Handle move commands
    if verb in ('go', 'move', 'travel'):
        # No direction provided
        if not args:
            print(f'{verb.capitalize()} where?')
            return current_room
        direction = args[0].title() # Capitalize first letter to match dictionary keys
        if direction in rooms[current_room]:
            current_room = rooms[current_room][direction] # Update room
            print(f'You went {direction}.')
            return current_room
        else:
            print(f"You can't go {direction}.") # Invalid move
            return current_room
    elif verb in ('get', 'grab', 'take'):
        if not args:
            print(f'{verb.capitalize()} what?\n'
                  'Correct usage: get "item name"')
            return current_room
        requested_item = ' '.join(args).title()
        if 'Item' in rooms[current_room]:
            if requested_item in rooms[current_room]['Item']:
                print(f'You took the {requested_item}.')
                inventory.append(rooms[current_room]['Item'])
                inventory.sort()
                if dialogue[requested_item]:
                    print('-' * 24)
                    print(dialogue[requested_item])
                del rooms[current_room]['Item']
                return current_room
            else:
                print(f'{requested_item} does not exist in the {current_room}.')
        else:
            print(f'There are no items to {verb} here.')
    # Handle exit command by setting current_room to 'Exit'
    elif verb in ('exit', 'quit'):
        current_room = 'Exit'
        return current_room
    # Display list of commands again
    elif verb in ('help', 'info', 'commands'):
        show_instructions(inventory)
    # Display every room
    elif verb == 'rooms':
        print('ROOMS: ')
        print('-' * 24)
        show_rooms(current_room, rooms, True)
    # If player has Supernatural Powers in their inventory, then open the powers menu
    elif verb == 'powers' and 'Supernatural Powers' in inventory:
        current_room = powers(inventory, current_room, rooms)
    # Invalid command entered
    else:
        print(f'"{user_command}" is not a valid command.\n'
              'Type "help"/"info"/"commands" to see available information and commands.')

    return current_room

def main():
    # Dictionary of all rooms, room connections, and states
    rooms = {
        'Lobby': {
            'East': 'Great Hall',
            'Player Entered': False},
        'Great Hall': {
            'North': 'Gallery',
            'South': 'Bedroom',
            'East': 'Dining Room',
            'West': 'Lobby',
            'Player Entered': False,
            'Item': 'Helmet'},
        'Dining Room': {
            'North': 'Kitchen',
            'West': 'Great Hall',
            'Player Entered': False,
            'Item': 'Steak'},
        'Kitchen': {
            'South': 'Dining Room',
            'East': 'Secret Room',
            'Player Entered': False,
            'Item': 'Flamethrower'},
        'Bedroom': {
            'North': 'Great Hall',
            'East': 'Bathroom',
            'Player Entered': False,
            'Item': 'Apple'},
        'Bathroom': {
            'West': 'Bedroom',
            'Player Entered': False,
            'Item': 'Toothbrush'},
        'Gallery': {
            'South': 'Great Hall',
            'East': 'Dungeon',
            'Player Entered': False,
            'Item': 'Body Armor'},
        'Dungeon': {
            'West': 'Gallery',
            'Player Entered': False,
            'Item': 'Villain'},
        'Secret Room': {
            'West': 'Kitchen',
            'Player Entered': False,
            'Item': 'Supernatural Powers'},
    }
    # Dictionary containing all dialogue for each room and item
    dialogue = {
        'Lobby':
            "\nThis room has severely damaged walls, smells of old carpet, and is eerily dark."
            "\nI should have brought a flashlight.",
        'Great Hall':
            "\nThe room is filled with old dusty furniture from centuries ago.",
        'Dining Room':
            "\nHow many people used to eat here? There are tons of seats and tables!",
        'Kitchen':
            "\nThere is a lot of expired food sitting out, almost like people had to evacuate immediately.",
        'Bedroom':
            "\nEverything is ripped up here, almost looks like claw marks? That cannot be good.",
        'Bathroom':
            "\nThis bathroom is completely wrecked, it reeks of mold, and there is water everywhere!",
        'Gallery':
            "\nThere are tons of painting all over the walls, who made all these?"
            "\nThey look pretty brutal and graphic, I would not want to meet whoever made these...",
        'Dungeon':
            None,
        'Secret Room':
            "\nThis place is pretty eerie...",
        'Apple':
            "A half-eaten apple, looks pretty recent to me.",
        'Body Armor':
            "This body armor looks pretty cool, aside from all the dents. "
            "Was this actually used in battle or something?",
        'Flamethrower':
            "A flamethrower? That's impressive. Whoever left this here might be someone I do not want to mess with.",
        'Helmet':
            "Looks brand new! I could probably use this as a hat!",
        'Steak':
            "Just raw meat.",
        'Toothbrush':
            "Surprisingly devious, reminds me of my high school days...",
        'Villain':
            None, # Villain is unobtainable
        'Supernatural Powers':
            'A glowing blue orb, interesting to say the least...'
    }
    current_room = 'Lobby' # Starting room
    inventory = []

    show_instructions(inventory) # Show commands at start
    # If start_with_powers is set to True, add Supernatural Powers to inventory and delete it from the room
    if start_with_powers:
        inventory.append('Supernatural Powers')
        del rooms['Secret Room']['Item']

    print('-' * 24)
    input('Press Enter to continue... ') # Wait for user to input before starting game

    # Main gameplay loop
    while True:
        check_status(current_room, inventory)  # Check if player has reached an end condition
        display_information(current_room, rooms, dialogue, inventory) # Show current state
        print('-' * 24)
        user_command = input('Enter command: ') # Prompt player for input
        current_room = evaluate_command(user_command, current_room, rooms, inventory, dialogue) # Process input

# Run game
if __name__ == '__main__':
    main()