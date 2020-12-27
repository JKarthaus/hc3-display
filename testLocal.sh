#!/bin/bash

echo "Local testing the great Heating Control LCD Display Connector"

export RABBIT_MQ_HOST=hc3-werkstatt
export RABBIT_MQ_QUEUE=hc-lcd-display

export DEMO_MODE=True

export WELCOME_TEXT="Heating Control III..."

#export LCD_ADDRESS=0x27

python3 lcdDisplay.py

