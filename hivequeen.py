#!/usr/bin/env python

import Tkinter
import json
import string 
import thread
import time

from googletv.proto import keycodes_pb2
import googletv
import discover

keydict = {
        'Escape': 'BACK',
        'Return': 'ENTER',
        ' ': 'SPACE',
        'BackSpace': 'DEL',
        'asciitilde': 'TILDE',
        'quoteleft': 'GRAVE',
        'quoteright': 'APOSTROPHE',
        'equal': 'EQUALS',
        'bracketleft': 'LEFT_BRACKET',
        'bracketright': 'RIGHT_BRACKET',
        'Up': 'DPAD_UP',
        'Down': 'DPAD_DOWN',
        'Left': 'DPAD_LEFT',
        'Right': 'DPAD_RIGHT',
        'F1': 'VOLUME_UP',
        'F2': 'VOLUME_DOWN',
        'F7': 'MEDIA_REWIND',
        'F8': 'MEDIA_PLAY_PAUSE',
        'F9': 'MEDIA_FAST_FORWARD',
        'F10': 'MUTE',
        }

STATUS_IDLE = 'idle'
STATUS_DISCOVERING = 'discovering...'
STATUS_CONNECTING = 'connecting...'

class Hivequeen(Tkinter.Frame):

    def __init__(self, root):
        self.status = Tkinter.StringVar()
        self.status.set(STATUS_IDLE)
        self.gtv = None
        Tkinter.Frame.__init__(self, root)
        self.root = root
        root.title('HIVEQUEEN')
        self.makeMenuBar()
        self.makeWidgets()
        #self.connect()

    def makeMenuBar(self):
        self.menu = Tkinter.Menu(self)
        self.master.config(menu=self.menu)
        self.tkMenu = Tkinter.Menu(self.menu)

        # File menu
        self.menu.add_cascade(label='File', menu=self.tkMenu)
        # Add items to the menu
        self.tkMenu.add_command(label='Connect', command=self.connect)
        self.tkMenu.add_command(label='Test Fling', command=self.fling)

    def makeWidgets(self):
        self.root.bind('<Key>', self.handle_key)

        self._statusLabel = Tkinter.Label(self.master, textvariable=self.status)
        self._statusLabel.grid(row=0, columnspan=2)

        self._discoverButton = Tkinter.Button(
                self.master, 
                text='Discover', 
                command=self.discoverPressed)
        self._discoverButton.grid(row=1, column=0)

        self._connectButton = Tkinter.Button(
                self.master, 
                text='Connect', 
                command=self.connectPressed)
        self._connectButton.grid(row=1, column=1)

        self._gtvBox = Tkinter.Listbox(
                self.master,
                selectmode=Tkinter.SINGLE)
        self._gtvBox.grid(row=2, columnspan=2, padx=5, pady=5,
                sticky=Tkinter.N+Tkinter.S+Tkinter.E+Tkinter.W)

        for i in range(3):
            Tkinter.Grid.columnconfigure(self.master, i, weight=1)
            Tkinter.Grid.rowconfigure(self.master, i, weight=1)

    def updateStatus(self, status):
        self.status.set("Status: {0}".format(status))

    def discoverPressed(self):
        self.updateStatus(STATUS_DISCOVERING)
        self._gtvBox.delete(0, Tkinter.END)
        thread.start_new(self._discoveryMethod, ())

    def _discoveryMethod(self):
        d = discover.Discovery()
        self.tvs = d.Discover()
        for tv in self.tvs:
            self._gtvBox.insert(Tkinter.END, tv[0])
        self.updateStatus(STATUS_IDLE)

    def connectPressed(self):
        def connectThread():
            self.updateStatus(STATUS_CONNECTING)
            if (self._gtvBox.curselection()):
                i = int(self._gtvBox.curselection()[0])
                self.connect(self.tvs[i][0], self.tvs[i][1])
            else:
                self.connect()

        thread.start_new(connectThread, ())

    def connect(self, 
            host='NSZGS7_C01_U2-NSZGS7U125121524.local.',
            port=9551,
            cert='cert.pem'):
        self.updateStatus('Connecting...')
        with googletv.AnymoteProtocol(host, cert, port=port) as self.gtv:
            self.updateStatus('Connected to {0} on port {1}'.format(host, port))
            while True:
               time.sleep(500) 

    def fling(self, uri='http://www.google.com'):
        if self.gtv:
            self.gtv.fling(uri)

    def handle_key(self, event):
        if not self.gtv:
            return
        self.gtv.keycode(getattr(keycodes_pb2, 'KEYCODE_SHIFT_LEFT'), 'up')
        self.shift('down', event)
        self.gtv.press(self.keycodeFromEvent(event))
        self.shift('up', event)

    def shift(self, action, event):
        if event.keysym not in keydict and event.char in string.uppercase:
            self.gtv.keycode(getattr(keycodes_pb2, 'KEYCODE_SHIFT_LEFT'), action)

    def keycodeFromEvent(self, event):
        print 'Event keysym: {0}'.format(event.keysym)
        if event.keysym in keydict:
            print 'using from keydict: {0}'.format(keydict[event.keysym])
            event.keysym = keydict[event.keysym]
        try:
            return getattr(keycodes_pb2, 'KEYCODE_%s' % event.keysym.upper())
        except Exception, e:
            print 'Unable to get key (char: {0}, keysm: {1}, exception: {2}'.format(
                    event.char, event.keysym, e)

def main():
    root = Tkinter.Tk()
    app = Hivequeen(root)
    app.mainloop()

if __name__ == '__main__':
    main()
