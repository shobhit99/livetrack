import datetime
def pack(key, args):
    if isinstance(args, str):
            message = "{%s: '%s'}" % (key, args)
    else:
        message = "{%s: %s}" % (key, args)
    return str.encode(message)

def secondsToDays(seconds):
    return str(datetime.timedelta(seconds=seconds))