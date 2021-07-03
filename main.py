import messenger_client as msg
import config
import logging
import logging.config
import scraper
import os
import datetime

# logging.basicConfig(filename='{}.log'.format(config.WD_GAME_ID), level=logging.DEBUG)
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'loggers': {
        '': {
            'level': 'NOTSET',
            'handlers': ['file_handler']
        }
    },
    'handlers': {
        'file_handler': {
            'level': 'DEBUG',
            'formatter': 'info',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{}.log'.format(config.WD_GAME_ID),
            'mode': 'a',
            'maxBytes': 1000000
        },
    },
    'formatters': {
        'info': {
            'format': '%(asctime)s-%(levelname)s-%(name)s::%(module)s|%(lineno)s:: %(message)s'
        }
    }
})


try:

    logging.debug("{}".format(datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")))

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

    logging.debug("PREV: {} {} {}".format(prev_season, prev_year, prev_phase))

    # check if date/phase are different
    this_tuple = scraper.get_date_and_phase()
    this_season = this_tuple[0].strip()
    this_year = this_tuple[1].strip()
    this_phase = this_tuple[2].strip()

    logging.debug("THIS: {} {} {}".format(this_season, this_year, this_phase))
    if this_season != prev_season or this_year != prev_year or this_phase != prev_phase:
        # send message with info
        # diplomatic phase:     U+1F52B     \N{pistol}
        # retreat phase:        U+1F4A2     \N{anger symbol}
        # build phase:          U+1F528     \N{HAMMER}


        phases = {
            "Diplomacy": "\N{pistol} DIPLOMACY: {}, {} \N{pistol}\n",
            "Retreats": "\N{anger symbol} RETREAT: {}, {} \N{anger symbol}\n\N{no entry sign} Communications Blackout\N{no entry sign}\n",
            "Builds": "\N{hammer} BUILD: {}, {} \N{hammer}\n\N{no entry sign} Communications Blackout \N{no entry sign}\n"
        }

        message_string = phases[this_phase].format(this_season, this_year)

        url = scraper.get_map_url()
        logging.debug("Sending message...")

        msg.login()
        msg.send_msg(url, message_string)

        save_file = open(save_name, "wt")
        save_file.write(this_season + '\n' + this_year + '\n' + this_phase + '\n')
        save_file.close()

    else:
        logging.debug("No progress detected.")

except Exception as e:
    logging.exception("An error has occurred.")
    exit(1)

exit(0)
