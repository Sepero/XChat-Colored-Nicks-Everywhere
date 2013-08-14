import xchat
import re
from collections import OrderedDict

__module_name__ = "colored_nicks_everywhere"
__module_version__ = "0.70"
__module_description__ = "Colors nicks in messages with the same color X-Chat uses to display nicks"

# Credit-
# Original Author: Paul "Joey" Clark
# Original URL: http://hwi.ath.cx/xchat_plugins/

display = (__module_name__ + " " + __module_version__ + " has been loaded.",
        "Module URL: https://github.com/Sepero/xchat_colored_nicks_everywhere/",
        "Author: Sepero - sepero 111 @ gmail . com",
        " Remote Python developer and Linux administrator for hire.",)
)

for line in display:
    print("\0034" + line + "\003")


normal_color = ""   # Adjust this if you display messages with a different color
#normal_color = "16"   # My config displays "Channel Message"s in bright-white

user_dict = OrderedDict()   # A cache of seen nicks and their coloring (actually a queue of least-to-most-recent speakers).
processed_lines = []   # A cache of lines that have already been colored.

# For stripping colors from a string
colorRe = re.compile(r"(||[0-9]{1,2}(,[0-9]{1,2}|))")
# For finding words in the message that could be a nick
nickRe = re.compile(r"[A-Za-z0-9_|/`'^\-\[\]\\]+")

def check_message(word, word_eol, userdata):
	nick_with_color = word[0]
	line_with_color = word[1]
	nick = colorRe.sub("",nick_with_color)
	line = colorRe.sub("",line_with_color)
	
	try:
		# Do nothing with already processed lines.
		processed_lines.remove(nick+line_with_color)
		return xchat.EAT_NONE
	except:
		pass
	
	# I was using xchat.get_list("users") here to get an up-to-date userlist for
	# the channel, but it caused a memory leak!  (X-Chat 2.8.6-2.1)
	# Maintain user_dict.
	if len(user_dict) > 2000:
		user_dict.popitem()
	
	try:
		del user_dict[nick]
	except:
		pass
	user_dict[nick] = nick_with_color + normal_color
	
	# Do nothing with lines which already contain color-codes.
	if line != line_with_color:
		return xchat.EAT_NONE
	
	# Replace nicks with colored nicks.
	for nick in user_dict:
		line = line.replace(nick, user_dict[nick])
	
	# Warning: emit_print() will get re-checked by check_message()!  But it should
	# reject it next time because it is in processed_lines.
	processed_lines.append(nick+line)
	xchat.emit_print("Channel Message", nick, line)
	return xchat.EAT_XCHAT

# A copy of the function from X-Chat:
# Currently unused function. (Previously used with xchat.get_list("users").)
rcolors = [ 19, 20, 22, 24, 25, 26, 27, 28, 29 ]
def color_of(nick):
	i=0
	sum=0
	while i<len(nick):
		c = nick[i]
		sum += ord(c)
		sum %= len(rcolors)
		i += 1
	return rcolors[sum]

xchat.hook_print("Channel Message", check_message)
