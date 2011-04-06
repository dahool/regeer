
def load_banlist(file):
    banlist = open(file)
    iplist = banlist.readlines()
    banlist.close()
    list = set([v.split(':')[0].strip() for v in iplist])
    return list

def save_banlist(file, list):
    banlist = open(file,'w')
    for e in list:
        banlist.write("%s:-1\n" % e)
    banlist.close()