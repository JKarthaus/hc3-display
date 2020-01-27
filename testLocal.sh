#!/bin/bash

echo "Local testing the great Heating Control LCD Display Connector"

export RABBIT_MQ_HOST=192.168.2.118
export RABBIT_MQ_QUEUE=hc-lcd-display

export DEMO_MODE=True

export WELCOME_TEXT="Heating Control III..."

#export LCD_ADDRESS=0x27

python3 lcdDisplay.py

