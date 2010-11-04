#! ../ve/bin/python

import re
import os
import sys
import time
import glob
import serial
import logging
import datetime
import optparse
import threading

proj = os.path.dirname(os.getcwd())
sys.path.append(proj)
sys.path.append(os.path.dirname(proj))
sys.path.append(os.path.join((proj, 've/')))

from django.core.management import setup_environ
from monitor import settings
setup_environ(settings)

from monitor.mon.models import Record

EOF = ';'
LF = '\n'
DEL = ','


class Monitor(object):

    def __init__(self, serials=None, **kwargs):
        self.baud = kwargs.get('baud')
        self.readonly = kwargs.get('readonly')
        self.timeout = kwargs.get('timeout', 0)
        self.commit = kwargs.get('commit', False)
        self.serials = serials
        self._tty_cache_of = 4
        self._tty_cache_timeout = None
        self._tty_cache = None

    def tty_list(self, **kwargs):
        try:
            return [serial.Serial(port, self.baud, timeout=self.timeout) for port in self.tty_names()]
        except IOError:
            if kwargs.get('rec', True):
                self._tty_cache_timeout = 0
                return self.tty_list(rec=False)
            else:
                raise

    def tty_names(self):
        return self.serials if self.serials else self.tty_scan()

    def tty_scan(self):
        if self._tty_cache is None or self._cache_timeout():
            self._tty_cache = glob.glob('/dev/ttyUSB*')
            self._tty_cache_timeout = self._timestamp() + self._tty_cache_of

        return self._tty_cache

    def _cache_timeout(self):
        return self._tty_cache_timeout is None or self._tty_cache_timeout < self._timestamp()

    def _timestamp(self):
        return time.mktime(datetime.datetime.now().timetuple())

    def run(self):
        tmp_names = self.tty_names()
        logging.info("Starting ... \nlistening on %s", tmp_names)

        while(1):
            res = list()
            for tty in self.tty_list():
                n = int(tty.inWaiting())
                if n > 0:
                    s = tty.read(n)
                    res.append(s)
                    if res[-1][-1] == EOF or self.readonly:
                        data = ''.join(res)
                        interp = Interpreter(data[:-1], commit=self.commit, readonly=self.readonly)
                        interp.start()
                        res = list()
                        # logging.debug(data)

            main = threading.currentThread()
            for t in threading.enumerate():
                if t == main:
                    continue
                logging.debug(t.getName())

            if tmp_names != self.tty_names():
                tmp_names = self.tty_names()
                logging.debug("now listening on %s", tmp_names)
            time.sleep(0.2)


class Interpreter(threading.Thread):

    def __init__(self, data, commit=False, readonly=False):
        threading.Thread.__init__(self)

        self.data = data
        self._data_fields_abbr = Record.data_fields_abbr()
        self.commit = commit
        self.readonly = readonly

    def run(self):
        if self.readonly:
            self.read()
            return

        r = Record(**self._interpret())
        if self.commit:
            r.save()
        else:
            r.created = datetime.datetime.now()
            logging.info("Record(created: %s, current: %s, volt: %s, temp: %s, light: %s)" %
                                (r.created, r.current, r.volt, r.temp, r.light))

    def read(self):
        logging.info("%s" % self.data)

    def _interpret(self):
        values = [d for d in self.data.split(DEL)]
        pairs = dict()

        for v in values:
            m = re.match(r'[a-zA-Z]+', v)
            if m is None:
                continue

            k = v[m.start():m.end()]
            try:
                k = self._data_fields_abbr[k.lower()]
            except KeyError:
                logging.debug("%s invalid key" % k)
                continue

            pairs[k] = v[m.end():]
        logging.debug("%s" % pairs)

        self.data_struct = pairs
        return pairs

if __name__=='__main__':
    option_list = (
        optparse.make_option('-c', '--commit',
            action = 'store_true',
            default = False,
            help = 'commit data to backend-db',
        ),
        optparse.make_option('-l', '--loglevel',
            type = 'choice',
            choices = ['INFO', 'DEBUG'],
            default = 'INFO',
        ),
        optparse.make_option('-r', '--readonly',
            action = 'store_true',
            default = False,
            help = 'dont interpret the data',
        ),
        optparse.make_option('-b', '--baud',
            default = 9600,
            type = int,
            help = 'set baud-rate',
        ),
    )

    parser = optparse.OptionParser(option_list=option_list)
    options, args = parser.parse_args()

    logging.basicConfig(level=logging.__getattribute__(options.loglevel))
    logging.debug(options)

    logging.info("Commit to database is %s" % options.commit)

    while(1):
        mon = Monitor(**options.__dict__)
        mon.run()

