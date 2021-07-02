import messenger_client as msg
import config
import time
import scraper
import os

if config.WD_GAME_ID == '':
    print('Please add your game ID to config.py')
    exit(1)

# msg.login()


while True:
    print("Polling...")

    save_name = "dipl_{}.txt".format(config.WD_GAME_ID)

    if not os.path.isfile(save_name):
        # Default save file, ensures first turn is sent
        save_file = open(save_name, "w")
        save_file.write("Spring\n1000\nDiplomacy\n")
        save_file.close()

    save_file = open(save_name, "rt")
    # Save file format:
    # 1     Season      <Autumn | Spring>
    # 2     Year        <19XX>
    # 2     Phase       <Diplomacy | Retreat | Build>

    prev_season = save_file.readline().strip()
    prev_year = save_file.readline().strip()
    prev_phase = save_file.readline().strip()

    save_file.close()

    # check if date/phase are different
    this_tuple = scraper.get_date_and_phase()
    this_season = this_tuple[0].strip()
    this_year = this_tuple[1].strip()
    this_phase = this_tuple[2].strip()
    if this_season != prev_season or this_year != prev_year or this_phase != prev_phase:
        # send message with info
        # diplomatic phase:     U+1F52B     \N{pistol}
        # retreat phase:        U+1F4A2     \N{anger symbol}
        # build phase:          U+1F528     \N{HAMMER}

        save_file = open(save_name, "wt")
        save_file.write(this_season + '\n' + this_year + '\n' + this_phase + '\n')
        save_file.close()

        phases = {
            "Diplomacy": "\N{pistol} DIPLOMACY\n",
            "Retreats": "\N{anger symbol} RETREAT\n",
            "Builds": "\N{hammer} BUILD\n"
        }

        message_string = phases[this_phase] + this_season + ", " + this_year

        url = scraper.get_map_url()
        print("Sending message: {}".format(message_string))
        msg.login()
        msg.send_msg(url, message_string)
    else:
        print("No progress detected. Sleeping for {} seconds.".format(config.POLL_TIME))

    time.sleep(int(config.POLL_TIME))
