"""
Black            \e[0;30m
Blue             \e[0;34m
Green            \e[0;32m
Cyan             \e[0;36m
Red              \e[0;31m
Purple           \e[0;35m
Brown            \e[0;33m
Gray             \e[0;37m
Dark Gray        \e[1;30m
Light Blue       \e[1;34m
Light Green      \e[1;32m
Light Cyan       \e[1;36m
Light Red        \e[1;31m
Light Purple     \e[1;35m
Yellow           \e[1;33m
White            \e[1;37m

"""
R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white


def default(text):
	return G + '[+]' + C + text + W

def error_(text):
	return R + '[-]' + C + text + W 


def alert(text):
	return R + '[!]' + C + str(text) + W