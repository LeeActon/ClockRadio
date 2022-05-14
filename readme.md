- Install Raspberry Pi OS Buster using Raspberry Pi Imager
  - SHIFT+CTRL+X to get advanced options
    - Enable SSH
    - Enable WIFI
    - Disable First run
- In Windows Terminal
  - ssh [pi@192.168.2.193](mailto:pi@192.168.2.193)
- sudo -s
  - apt-get install git
  - apt-get install python3-pip
  - pip3 install pygame
- From [https://shop.pimoroni.com/products/hyperpixel-round](https://shop.pimoroni.com/products/hyperpixel-round)
  - git clone [https://github.com/pimoroni/hyperpixel2r](https://github.com/pimoroni/hyperpixel2r)
  - cd hyperpixel2r
  - sudo ./install.sh
- From [https://github.com/pimoroni/hyperpixel2r-python](https://github.com/pimoroni/hyperpixel2r-python)
  - git clone https://github.com/pimoroni/hyperpixel2r-python
  - cd hyperpixel2r-python
  - sudo ./install.sh
  - edit /boot/config.txt
    - # Force 640x480 video for Pygame / HyperPixel2r
    - hdmi\_force\_hotplug=1
    - hdmi\_mode=1
    - hdmi\_group=1
- sudo reboot ����reboot
- sudo apt install libsdl2-dev
- sudo apt-get install python-smbus i2c-tools
- apt-get install libsdl2-image-2.0-0
- sudo apt-get install libsdl2-ttf-2.0-0 (for fonts)
- pip3 install debugpy
- For touch:
  - From: [https://github.com/pimoroni/hyperpixel2r-python/issues/6](https://github.com/pimoroni/hyperpixel2r-python/issues/6)
  - sudo pip3 install python-uinput
  - sudo pip3 install evdev
- Connect to shares on laptop:
  - Sudo vi /etc/fstab
  - //LEE-YOGA/Users/Lee/source/repos/ClockRadio /home/pi/ClockRadio.dev cifs username=lee,password=password,iocharset=utf8
  - //LEE-YOGA/Users/Lee/Shared /home/pi/Lee-Shared cifs username=lee,password=password,iocharset=utf8

