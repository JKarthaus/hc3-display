#!/usr/bin/env python
import lcddriver 
from time import *
import pika
import sys
from threading import Thread
import threading
import time
import logging
import os

lcd = None


rabbitMqHost = os.environ['RABBIT_MQ_HOST']
rabbitMqQueue = os.environ['RABBIT_MQ_QUEUE']
demoMode = eval(os.environ.get('DEMO_MODE', False))

rowData = [" "," "," "," "," "]

connection = pika.BlockingConnection
# -------------------------------------------------------------------------------------------------------
def writeDataToDisplay():
    global lcd
    global rowData
    global demoMode
    
    logging.info("writeDataToDisplay Thread startet...")
    ct = threading.currentThread()
    lcd = lcddriver.lcd()
    while getattr(ct, "do_checking", True):
        if not demoMode:
            lcd.lcd_clear()
        else:
            logging.info("----------------------------------")

        rowCount = 0
        for row in rowData:
            if not demoMode:
                lcd.lcd_display_string(row, rowCount)
            else:
                logging.info("Write: " + row  + " on LCD row:" + str(rowCount))
            rowCount +=1
        time.sleep(10)
# -------------------------------------------------------------------------------------------------------


def openConnection():
    global connection
    global rabbitMqHost
    global rabbitMqQueue

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMqHost))
    channel = connection.channel()
    channel.basic_consume(queue=rabbitMqQueue,on_message_callback=callback)
    logging.info("Waiting for Messages on Queue:" + rabbitMqQueue)
    channel.start_consuming()
# -------------------------------------------------------------------------------------------------------


def closeConnection():
    global connection
    connection.close()
# -------------------------------------------------------------------------------------------------------


def callback(ch, method, properties, body):
    global rabbitMqQueue
    global rowData

    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logging.debug("Message arrived")
        stringBody = "".join(map(chr, body))

        if stringBody.find("=") != -1:
            if demoMode:
                logging.info("Rceived:" + stringBody)
            row = stringBody[0:stringBody.find("=")]
            rowData[int(row)] = stringBody[stringBody.find("=")+1:]
        else:
            logging.info("Message on Channel: " + rabbitMqQueue +
                         " has an unexpectedly Format -> expecting ROW=DATA")
    except BaseException as error:
        logging.error(error)
# -------------------------------------------------------------------------------------------------------


def main():
    global lcd
    logging.basicConfig(level=logging.INFO)
    logging.info("---------------------------------------------")

    rowData[0] = " "
    rowData[1] = os.environ.get('WELCOME_TEXT', "booting...")
    rowData[2] = " "
    rowData[3] = " "


    if not demoMode:
        logging.info("LCD initialised...")
        lcd = lcddriver.lcd()
        lcd.lcd_clear()
        # Start anf join the output Thread
        outputThread = Thread(target=writeDataToDisplay)
        outputThread.join()
        outputThread.daemon = True
        outputThread.start()
    else:
        logging.info("lcdDisplay Connector Started in DEMO MODE")


    openConnection()

    logging.info('Finished')
    closeConnection()
    logging.info("---------------------------------------------")


if __name__ == '__main__':
    try:
        main()
    except:
        logging.info("---------------------------------------------")
        logging.info("-- CRITICAL ERROR OCCURED...")
        logging.info("---------------------------------------------")
        sys.exit(2)
