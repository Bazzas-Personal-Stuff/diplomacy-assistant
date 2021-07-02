from fbchat import *
import fbchat
import config
import getpass
import urllib.request as url


fb_client: Client
fb_thread: int


def login():
    global fb_client
    is_logged_in = False
    if config.FB_EMAIL != '' and config.FB_PASSWORD != '':
        try:
            fb_client = Client(config.FB_EMAIL, config.FB_PASSWORD, max_tries=1)
            is_logged_in = True
        except (fbchat.FBchatException, fbchat.FBchatUserError):
            print("Failed login")

    while not is_logged_in:
        try:
            email = input("Facebook email: ")
            password = getpass.getpass("Facebook password: ")
            fb_client = Client(email, password, max_tries=1)
            is_logged_in = True
        except (fbchat.FBchatException, fbchat.FBchatUserError):
            print("Failed login")

    global fb_thread
    fb_thread = int(config.FB_GROUP_THREAD_ID)


def send_msg(map_url: str, message: str):
    global fb_client
    if fb_client is None:
        login()

    url.urlretrieve(map_url, "map.png")
    fb_client.sendLocalImage("map.png", message, fb_thread, fbchat.ThreadType.GROUP)

