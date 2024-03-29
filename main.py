#! /usr/bin/env python

# Check for root user login
import os, sys
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")

# Get your username (not root)
import pwd
uname=pwd.getpwuid(1000)[0]

# The remastering process uses chroot mode.
# Check to see if this script is operating in chroot mode.
# /home/mint directory only exists in chroot mode
is_chroot = os.path.exists('/home/mint')
dir_develop=''
if (is_chroot):
	dir_develop='/usr/local/bin/develop'
	dir_user = '/home/mint'
else:
	dir_develop='/home/' + uname + '/develop'
	dir_user = '/home/' + uname

# Everything up to this point is common to all Python scripts called by shared-*.sh
# =================================================================================

def add_pkg (packages):
    os.system ('echo INSTALLING ' + packages)
    os.system ('apt-get install -qq ' + packages)

def change_text (filename, text_old, text_new):
    # Replaces text within a file
    text=open(filename, 'r').read()
    text = text.replace(text_old, text_new)
    open(filename, "w").write(text)

os.system ('echo ==============================')
os.system ('echo BEGIN ADDING SECURITY FEATURES')

add_pkg ('gufw')

os.system ('echo Pre-activate the firewall')
change_text ('/etc/ufw/ufw.conf', 'ENABLED=no', 'ENABLED=yes')

add_pkg ('keepass2')

os.system ('echo FINISHED ADDING SECURITY FEATURES')
os.system ('echo =================================')
