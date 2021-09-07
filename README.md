# epdtext

A simple display manager app for the [WaveShare 2.7in e-Paper HAT](https://www.waveshare.com/2.7inch-e-paper-hat.htm)

The app provides a number of screens that can be displayed on the e-paper HAT, and allows switching between them with the builtin buttons.

The framework is extensible, so you can write your own screens as well, each screen is a Python module providing the `handle_btn_press` and `print_to_display` functions.

## Setup on Raspberry Pi OS

* First, enable the SPI inferface on the Pi if you haven't already.
* Then, install the Python requirements

```shell
sudo apt install python3-pip python3-pil python3-numpy python3-gpiozero
```

* Then install the drivers for Python

```shell
git clone https://github.com/waveshare/e-Paper ~/e-Paper
cd ~/e-Paper/RaspberryPi_JetsonNano/python
python3 setup.py install
```

* Check out the code if you haven't already:

```shell
git clone https://github.com/tsbarnes/epdtext.git ~/epdtext
```

* Install the remaining Python dependencies
```shell
cd ~/epdtext
sudo pip3 install -r requirements.txt
```

* Then (optionally) create local_settings.py and add your settings overrides there.
* Also optional is installing the systemd unit.

```shell
cp ~/epdtext/epdtext.service /etc/systemd/system
sudo systemctl enable epdtext
```

## Usage

To start up the app, run this command:
```shell
cd ~/epdtext
python3 app.py
```
