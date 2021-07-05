#!/usr/bin/env bash
# turn on camera
sudo raspi-config

# enable IC2
sudo raspi-config

# basic, update, git, python3 install
sudo apt-get update

sudo apt install git
#After this operation, 32.9 MB of additional disk space will be used.
#Do you want to continue? [Y/n] y



sudo apt-get install -y vim git python3-pip

# clone avicar-poc git
git clone https://bozam@github.com/fittico/avicar-poc


# uv4l installation
curl http://www.linux-projects.org/listing/uv4l_repo/lpkey.asc | sudo apt-key add -
sudo chmod 777 /etc/apt/sources.list
sudo echo "deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch main" >>/etc/apt/sources.list

sudo apt-get install autoconf
# Do you want to continue? [Y/n]



wget http://www.linux-projects.org/listing/uv4l_repo/lrkey.asc && sudo apt-key add ./lrkey.asc

echo "deb [trusted=yes] http://www.linux-projects.org/listing/uv4l_repo/raspbian/ wheezy main" >>/etc/apt/sources.list
sudo apt-get update

sudo apt-get install -y uv4l uv4l-raspicam uv4l-raspicam-extras uv4l-dummy

sudo apt-get install uv4l-server
# Do you want to continue? [Y/n]


# if there is an issue with installation of uv4l-server due to the missing libssl1.0.0 library which seems to be a fix dependency then this library should be installed manually by:
# wget http://security.debian.org/debian-security/pool/updates/main/o/openssl/libssl1.0.0_1.0.1t-1+deb8u12_armhf.deb
# sudo apt install ./libssl1.0.0_1.0.1t-1+deb8u12_armhf.deb
# then try again installation of uv4l-server by:
# sudo apt-get install uv4l-server


# webRTC extension for uv4l-server
sudo apt-get install uv4l-webrtc

# Do you want to continue? [Y/n]

# install rpi.gpio
sudo apt-get install rpi.gpio


sudo apt-get install python-pigpio python3-pigpio
# Do you want to continue? [Y/n]

pip3 install -r ~/avicar-poc/requirements.txt

sudo mv /etc/uv4l/uv4l-raspicam.conf /etc/uv4l/uv4l-raspicam.conf.bak
sudo cp ~/avicar-poc/uv4l-raspicam.conf /etc/uv4l/uv4l-raspicam.conf

sudo cp ~/avicar-poc/controller.service /etc/systemd/system/

sudo systemctl enable controller.service


# PIGPIOD needs to start on boot

sudo pigpiod
sudo systemctl start uv4l_raspicam.service
sudo systemctl start controller.service
# enable wireless
sudo systemctl enable wpa_supplicant.service
sudo reboot


# Configuring Your Pi for I2C
sudo apt-get install python-smbus
# Do you want to continue? [Y/n]

sudo apt-get install i2c-tools


# Python Installation of ServoKit Library
sudo pip3 install adafruit-circuitpython-servokit


# check if this is necessary
sudo apt-get install git build-essential python-dev
# Do you want to continue? [Y/n]


#cd ~
#git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git
#cd Adafruit_Python_PCA9685
#sudo python setup.py install

sudo pip3 install adafruit-pca9685

sudo pip3 install keyboard

# ngrok installation - use if needed



