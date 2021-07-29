import os
import dotenv
import scraper
import sys

dotenv.load_dotenv()
WD_GAME_ID = os.getenv('WD_GAME_ID')


def get_status() -> (str, str, bool, int, str):
    """Returns: Phase string, Map URL, Communications, Colour, Date"""
    print("Polling...")
    save_name = "dipl_{}.txt".format(WD_GAME_ID)

    if not os.path.isfile(save_name):
        # Default save file, ensures first turn is sent
        with open(save_name, "wt") as save_file:
            save_file.write("Spring\n1000\nPre-game\n")

    # Save file format:
    # 1     Season      <Autumn | Spring>
    # 2     Year        <19XX>
    # 2     Phase       <Diplomacy | Retreat | Build>
    with open(save_name, "rt") as save_file:
        prev_season = save_file.readline().strip()
        prev_year = save_file.readline().strip()
        prev_phase = save_file.readline().strip()

    # check if date/phase are different
    try:
        this_tuple = scraper.get_date_and_phase()
        this_season = this_tuple[0].strip()
        this_year = this_tuple[1].strip()
        this_phase = this_tuple[2].strip()
        if this_season != prev_season or this_year != prev_year or this_phase != prev_phase:
            # send message with info
            # diplomatic phase:     U+1F52B     \N{pistol}
            # retreat phase:        U+1F4A2     \N{anger symbol}
            # build phase:          U+1F528     \N{HAMMER}

            phases = {
                "Diplomacy": "\N{pistol} DIPLOMACY \N{pistol}\n",
                "Retreats": "\N{anger symbol} RETREAT \N{anger symbol}\n",
                "Builds": "\N{hammer} BUILD \N{hammer}\n",
                "Pre-game": "\N{alarm clock} PRE-GAME \N{alarm clock}\n"
            }

            colors = {
                "Diplomacy": 0x47b484,
                "Retreats": 0xf2454b,
                "Builds": 0xf7a432,
                "Pre-game": 0x7289da
            }

            message_string = phases[this_phase]
            color = colors[this_phase]
            comms = True if this_phase == "Diplomacy" or "Pre-game" else False
            date = "{}, {}".format(this_season, this_year)

            url = scraper.get_map_url()
            print("Sending message: {} {} {}".format(message_string, date, url))

            with open(save_name, "wt") as save_file:
                save_file.write("{}\n{}\n{}\n".format(this_season, this_year, this_phase))

            return message_string, url, comms, color, date
        else:
            print("No progress detected.")
            return None

    except Exception as e:
        print(e, file=sys.stderr)
        return None
