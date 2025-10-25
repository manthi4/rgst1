from art import text2art
import datetime

##assets
blank_face=\
    "        ____________            ____________        \n"+\
    "       /            \          /            \       \n"+\
    "      |      /\      |        |      /\      |      \n"+\
    "      |     /[]\     |        |     /[]\     |      \n"+\
    "      |     \__/     |        |     \__/     |      \n"+\
    "       \____________/          \____________/       \n"+\
    "                         /\                         \n"+\
    "                        /  \                        \n"

f_hello_world = text2art("hellow World!")
f_hi = text2art("Hello!")

def get_f_time(just_time=False):
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H : %M : %S" )
    f_time = text2art(formatted_time)
    if just_time:
        return f_time
    formatted_date = now.strftime("%Y : %m : %d")
    f_date = text2art(formatted_date)
    f_combo = f_date + f_time
    return f_combo