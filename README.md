# Kangaroo-Surfer
this is a nightmare so far
https://www.waveshare.com/w/upload/5/54/WM8960_Audio_HAT_User_Manual_EN.pdf
# NOTE: the driver you want depends on kernel verssion
I used a version of debeian stretch that kad kernel 4.19

# any version less than 5 use this
git clone -b rpi-4.9.y https://github.com/waveshare/WM8960-Audio-HAT.git
# any version over 5 use this
git clone https://github.com/waveshare/WM8960-Audio-HAT

# install python 2.7
https://www.how2shout.com/linux/how-to-install-python-2-7-on-ubuntu-20-04-lts/

# pip install
sudo apt update 
sudo apt install curl 
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
sudo python2 get-pip.py

# install this thing
sudo apt-get install python-dev

# idk what this is but pyalsaaudio wont install without it
sudo apt-get install libasound2-dev

# alsaaudio install
pip install pyalsaaudio

# rpi gpio install
pip install rpi.gpio

# testing code 
https://www.waveshare.com/wiki/File:WM8960_Audio_HAT_Code.tar.gz
