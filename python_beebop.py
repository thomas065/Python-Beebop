# Python Beebop Text Game


from pygame import mixer
import sys
import random
import time
from termcolor import colored, cprint
from colorama import init
init()
mixer.init()
mixer.music.load('footsteps.wav')
mixer.music.play()

balance = 0


def blink_once():
    sys.stdout.write('\r---> THIS WAY <---')
    time.sleep(0.5)
    sys.stdout.write('\r                  ')
    time.sleep(0.5)


def blink(number):
    for x in range(0, number):
        blink_once()


class Villain():
    def __init__(self, name,  bounty, hit_points, criminal_record):
        self.name = name
        self.bounty = bounty
        self.hit_points = hit_points
        self.criminal_record = criminal_record


class Boss(Villain):
    def __init__(self, name, bounty, hit_points, criminal_record, weapon):
        super().__init__(name, bounty, hit_points, criminal_record)
        self.weapon = weapon

    def molotov(self, molotov):
        print(self.__class__.__name__,  "casts", molotov)


def bounty_board():
    print("")
    print("------------------------------------------")
    print("|         === Big Shot Bounty ===        |")
    print("------------------------------------------")
    print("| 1. Random Bounty  | 2.    FIGHT!       |")
    print("------------------------------------------")
    print("------------------------------------------")
    print("| 3.  Big Bosses    | 4.    Logout       |")
    print("------------------------------------------")


yes_list = ['yes', 'y', 'Yes', 'YES']
no_list = ['no', 'No', 'n', 'NO']


class Player():
    def __init__(self, name):
        self.health = 100
        self.name = name
        self.wins = 0

    def attack_dmg(self, damage_amt, attacker):
        if (damage_amt > self.health):
            fatality = abs(self.health - damage_amt)
            self.health = 0
            if (fatality > 0):
                print("{0} takes fatal damage from {1}, with {2} fatality!"
                      .format(self.name.capitalize(), attacker, fatality))
            else:
                print("{0} takes fatal damage from {1}!"
                      .format(self.name.capitalize(), attacker))
        else:
            self.health -= damage_amt
            print("{0} takes {1} damage from {2}!"
                  .format(self.name.capitalize(), damage_amt, attacker))

    def cola(self, heal_amt):
        if (heal_amt + self.health > 100):
            self.health = 100
            print("{0} healed back to full health!"
                  .format(self.name.capitalize()))
        else:
            self.health += heal_amt
            print("{0} healed for {1}!"
                  .format(self.name.capitalize(), heal_amt))


def parse_int(input):
    try:
        int(input)
        return True
    except ValueError:
        return False


def selection():
    valid_input = False
    while valid_input is False:
        print()
        choice = input("Select an attack: ")
        if (parse_int(choice) is True):
            return int(choice)
        else:
            print("Select again.")


def mob_mechanics(health):
    sleep_time = random.randrange(2, 5)
    cprint("zz::|..zZ|..::|LOADING|::..|Zz..|::zz", 'blue')
    time.sleep(sleep_time)

    if (health <= 35):
        result = random.randint(1, 6)
        if (result % 2 == 0):
            return 3
        else:
            return random.randint(1, 2)
    elif (health == 100):
        return random.randint(1, 2)
    else:
        return random.randint(1, 3)


def bounty_game(villain, human):
    global balance
    gaming = True
    current_player = villain

    while gaming:
        if (current_player == villain):
            current_player = human
        else:
            current_player = villain

        print()
        print("You have {0} health remaining and your "
              "opponent has {1} health remaining." .format(human.health, villain.health))
        print()

        if (current_player == human):
            print("Actions Available: ")
            print("1) Roundhouse Kick - shock damage.")
            print("2) Plasma Shot - Random damage: based on chance!")
            print("3) Cola - Restores some health.")
            key_press = selection()
        else:
            key_press = mob_mechanics(villain.health)

        if (key_press == 1):
            mixer.music.load('strong_punch.wav')
            mixer.music.play()
            damage = random.randrange(18, 25)
            if (current_player == human):
                villain.attack_dmg(damage, human.name)
            else:
                human.attack_dmg(damage, villain.name)
        elif (key_press == 2):
            mixer.music.load('plasma_shot.wav')
            mixer.music.play()
            damage = random.randrange(10, 35)
            if (current_player == human):
                villain.attack_dmg(damage, human.name)
            else:
                human.attack_dmg(damage, villain.name)
        elif (key_press == 3):
            heal = random.randrange(18, 25)
            current_player.cola(heal)
        else:
            print("Select again.")

        if (human.health == 0):
            mixer.music.load('fatality.wav')
            mixer.music.play()
            cprint("Sorry Cowboy, maybe next time! You've lost credits....", 'red')
            villain.wins += 1
            balance -= 15000
            gaming = False
            print(f"Your balance is: {balance}")
            if balance < 0:
                cprint(
                    "You seem to be in debt Cowboy, you might want to bring in more bounties.", 'yellow')

        if (villain.health == 0):
            mixer.music.load('Finish_Him.wav')
            mixer.music.play()
            cprint(
                "Congratulations, you brought in a bounty and earned credits!", 'green', 'on_red')
            human.wins += 1
            balance += 15000
            gaming = False
            print(f"Your balance is: {balance}")


def beebop():
    mixer.music.stop()
    cprint("YOU'R NOT TAKING ME IN THAT EASY !!!", 'red')
    villain = Player("Villain")
    name = input("What's your name again?: ")
    print(f"It's not gonna matter once I'm done with you, {name}.")
    time.sleep(2)
    mixer.music.load('fight.wav')
    mixer.music.play()
    print()
    human = Player(name)

    keep_playing = True
    while (keep_playing is True):
        print("Current Score:")
        print("You - {0}".format(human.wins))
        print("Villain - {0}".format(villain.wins))

        villain.health = 100
        human.health = 100
        bounty_game(villain, human)
        print()
        response = input("Play Again?(Y/N)")
        if (response.lower() == "n"):
            break


def python_beebop():
    # start scene

    global balance

    print()
    print("You walk down a corridor.")
    print("A blinking sign illuminates a door slightly ajar.")
    print(colored("---> THIS WAY <---", 'red')), blink(6)
    print()
    user = input("You hear a voice, 'Come in and sit'.\nWhat is your name? ")
    print()
    print(f"{user},")
    cprint("Welcome to Python Beebop!", 'yellow')
    print()

    print("You enter a hyperbolic chamber, what looks like to be a guy in a lab coat sets you comfortably in the chair and straps you in.")
    print("You feel slightly nervous. Over the loud speaker you hear a female voice, 'Everything is in order Doctor!'.")
    print("The Doctor turns to you as he retrofits an Oculus mask over your head, 'Please relax, your new adventure awaits.")
    print("Count backwards from 10 and we'll see you when you wake up.'.\nYou close your eyes and start counting, 10, 9, 8,...")
    time.sleep(3)

    n = 7
    while n > 0:
        time.sleep(1), print(n)
        n = n - 1
    print(f"{n}....you begin to wake up.")
    print()
    play = input("Would you like to play? Y/N: ")
    print()

    mixer.music.load('cowboy_beebop.mp3')
    mixer.music.play(-1)
    mixer.music.set_volume(0.1)

    while True:
        print()
        print("Press 'P' to continue music and play program")
        print("Press 'X' to stop music and continue program")
        music = input("Enter: ")

        if music.lower() == 'p':
            break

        elif music.lower() == 'x':
            # Stop the mixer
            mixer.music.stop()
            break

    if play.lower() in yes_list:
        print("The year is 2042, Earth is in peril. The 'Great Divide' as it were has happened.")
        print("The rich and powerful have fled off-world to terraformed planets of Utopia, engineered")
        print("by Jeff Pythose and Pylon Musk, leaving the less fortunate to rot and wage war amongst themselves on Earth.")
        print(f"YOU...{user} are a Bounty Hunter sworn by Oath to bringing evil-doers to the RJSOA,\notherwise known as the Reformed Justice System of America.")
        time.sleep(6)
        print()
        print("You slowly stand up from your chair.")
        time.sleep(3)

        chance = int(input("Chance roll between 1 and 10: "))

        if chance > 7 and chance <= 10:
            print("you feel fine.")
        elif chance >= 4 and chance <= 7:
            time.sleep(1)
            print("You feel strange but everything checks okay.")

        elif chance > 1 and chance < 4:
            time.sleep(3)
            print("You don't feel so hot and need to eat something.")
        else:
            print("You have collapsed.")
            exit()

    elif play in no_list:
        print("sorry to see you go.")
        exit()

    choice = input("(female voice) Are you okay? ")
    time.sleep(2)
    print()

    while True:

        if choice.lower() in yes_list or choice.lower() in no_list:
            print(
                "Before you go, look over there by the table and crack open that cola. It will rejuvinate you.")
            print("By the way, My name is Doc. Start your quest by visiting the Bounty Board right outside those double doors.")
            print("Good luck!\n(you leave the room.)")
            time.sleep(2)
            print("You grab a refreshing Cola and just as Doc said, you see the Bounty Board\nLet's see, who shall I bring in?")
            print()
            break

        else:
            print("Invalid choice!")
            break

    while True:
        global balance
        hp = 250

        name = (
            "Asimov Solanson", "Abdul Hakim", "Bakri Chinva",
            "Mao Yenrai", "Faye Valentine", "Teddy Bomber",
            "Chessmaster Hex", "Baker Panchorero"
        )

        boss = (
            "Vicious", "Julia", "Piccaro Calvino", "Domino Walker",
            "Doctor Londes", "Ajiz"
        )

        crime = (
            "Bank Robbery", "Murder", "Tax Evasion", "Child Kidnapping",
            "Agricultural Activist", "Explosive Teddy Bears", "Crime Syndicate"
        )

        bounty_board()
        option = input("Choose an Option: ")

        if option == "2":
            beebop()

        elif option == "1":
            thug = Villain(random.choice(name), 15000,
                           hp, random.choice(crime))
            print("\nName:"), cprint(f"{thug.name}", 'yellow')
            print(
                f"Credits: {thug.bounty} \nHP: {thug.hit_points} \nFelony: {thug.criminal_record}")

        elif option == "3":
            mob = Boss(random.choice(boss), 35000,  hp,
                       random.choice(crime), "molotov")
            print("\nName:"), cprint(f"{mob.name}", 'red')
            print(
                f"Credits: {mob.bounty} \nHP: {mob.hit_points} \nFelony: {mob.criminal_record} \nWeapon: {mob.weapon}")

        elif option == "4":
            print(f"\nGoodbye {user}!")
            break

        else:
            print("??")


python_beebop()
