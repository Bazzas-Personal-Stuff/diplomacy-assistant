from fbchat import *
import fbchat
import config
import urllib.request as url


fb_client: Client


def login(email=config.FB_EMAIL, password=config.FB_PASSWORD):
    global fb_client
    fb_client = fbchat.Client(email, password)


def send_msg(map_url: str, message: str, thread=config.FB_GROUP_THREAD_ID):
    global fb_client
    if fb_client is None:
        login()

    url.urlretrieve(map_url, "map.png")
    fb_client.sendLocalImage("map.png", message, thread, fbchat.ThreadType.GROUP)

