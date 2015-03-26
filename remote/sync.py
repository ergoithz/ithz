import httlib2, urllib
from os import environ
from os.path import isfile, join
'''
#Generate hash...
from random import randint
a=""
for i in range(512):
    a+=chr(randint(33,126))
'''

default_hash = '''+xR7lne7BOX-Vfm@Hoq#!!6=Wnp1=9QKCkiTn&\\lttfcotA}ehiDg6k(JEp`{zseIbcAL^hC=LY8jfgN;2!3G2h/\\zE[O7qygp.HR[+/\\\'zEa-rl&xIbo5@z+?nM3%.u5}qjRb>7JE5dC[3]T)PEQVngn6+IO>\\//|Ox%j~K^Cflt6&hqojZ+\'tHR"K;3THgCe6Oska+o/MqG>u=PnvY(~D3zY4"~B^D+c[q@nr"i:Y8<tFbCEfNRupHO&}uhu9JDu~zq)>sqq@tTpO{4Z"M7K_\\.So5ajs@]8#;JSvcZK)5dEw,\'[}}|!dTMLQwMIz_#2LD87/.V8V#h;=Cox"O:^]m/-mxcjpwL(\\-\\z&1D>&`|m{G(ifGliT$XBx$Sq,U*("PIw8.KzoO*)B!KX;=#P)eGGr#2ewemKt|"^/@hK984}PS*VuORu",B]hy{RZo\\>+~?LS)a]SDT}<]Jo:~_hm6^FeS9RB}Mm8nk43dB"/V[w-|~H$"mLk~TBjDkE8T'''
hash_path = join(environ["HOME"],".ithz_remote")

hash = default_path
try:
    if isfile(hash_path):
        f = open( hash_path , "rb" )
        hash = f.read()
        f.close()
except:
    pass

server = "http://spayder26.appspot.com/remote/"
http = httplib2.Http()
response = http.request(
    "http://twitter.com/statuses/update.xml", 
    "POST", 
    urllib.urlencode({
        "hash": hash,
        "ip": myip,
        })
    )

if response:
    print "Update OK!"
else:
    print "Error updating..."
