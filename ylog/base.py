import atexit
import datetime
import os
try:
    import queue
except ImportError:
    import Queue as queue  # fallback for Python 2.x
import sys
import threading
import time


LOG_LEVEL_PROD = 1
LOG_LEVEL_DEBUG = 2

# TODO(niklas9):
# * add to docs that Log() is a singleton class
# * make logging format customizable
# * add option to make it blocking, no threading
# * add thread id to log fmt, needs to be supplied to the logging method
#   to make sure it's not mixed up with ylog's threads
# * add coloring with colored package ? really minimalistic? :) should
#   be a separate formatter instead later ?


class InvalidLogLevelException(Exception):  pass

class Log(object):

    TIMESTAMP_FMT = '%Y-%m-%dT%H:%M:%S.%f+00:00'  # utc, iso-8601
    LOG_FMT = '%s|%s|%s|%s\n'  # timestamp, pid, debug level, msg
    LEVEL_INFO = 'INFO'
    LEVEL_DEBUG = 'DEBUG'
    LEVEL_WARNING = 'WARN'
    LEVEL_ERROR = 'ERROR'
    LOG_FLUSH_TIMEOUT_CHECK = 0.1  # seconds
    LOG_FLUSH_TIMEOUT_WARN = 0.5  # seconds
    LOG_FLUSH_TIMEOUT = 5  # seconds
    FILEMODE_APPEND = 'a'
    FILE_ENCODING_UTF8 = 'utf-8'

    log_level = None
    log_fh = None
    queue = None
    use_stdout = None
    _instance = None  # placeholder for singleton instance
    _init_executed = False

    def __init__(self, log_level=None, log_file=None, use_stdout=True,
                 re_init=False):
        # TODO(niklas9):
        # * _init_executed is a hack, how to make sure constructor is only
        #   executed once for a singleton class? is this the way?
        if not re_init and self._init_executed:  return
        if log_level is None:
            log_level = LOG_LEVEL_DEBUG  # default to debug
        if log_level not in (LOG_LEVEL_PROD, LOG_LEVEL_DEBUG):
            raise InvalidLogLevelException(log_level)
        self.log_level = log_level
        self.queue = queue.Queue()  # FIFO
        # TODO(niklas9):
        # * make it scream if not able to touch suggested log_file
        if log_file is not None:
            self.log_fh = open(log_file, mode=self.FILEMODE_APPEND,
                               encoding=self.FILE_ENCODING_UTF8)
        self.use_stdout = use_stdout
        t = threading.Thread(target=self._log_worker)
        t.daemon = True
        # NOTE(niklas9):  * make sure log queue is emptied before exit
        atexit.register(self._wait_until_queue_is_empty)
        t.start()
        self._init_executed = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # TODO(niklas9):
            # * why doesn't it work by passing *args and **kwargs to
            #   the call below in Python 3.x?
            cls._instance = super(Log, cls).__new__(cls)
        return cls._instance

    def info(self, msg):
        self._log(self.LEVEL_INFO, msg)

    def debug(self, msg):
        if self.log_level == LOG_LEVEL_DEBUG:
            self._log(self.LEVEL_DEBUG, msg)

    def warn(self, msg):
        self._log(self.LEVEL_WARNING, msg)

    def warning(self, msg):  self.warn(msg)

    def error(self, msg):
        self._log(self.LEVEL_ERROR, msg)

    def err(self, msg):  self.error(msg)

    def _log(self, log_level, msg):
        self.queue.put((log_level, msg))

    def _output(self, msg):
        if self.use_stdout:
            sys.stdout.write(msg)
        if self.log_fh is not None:
            self.log_fh.write(msg)
            self.log_fh.flush()

    def _log_worker(self):
        while True:
            try:
                log_level, msg = self.queue.get(block=True)
            except queue.Empty:
                continue
            finally:
                # TODO(niklas9):
                # * move time to _log ? then we get the right time of the
                #   actual log entry happening.. not when the worker
                #   thread picks it up..
                ts = datetime.datetime.utcnow().strftime(self.TIMESTAMP_FMT)
                msg = self.LOG_FMT % (ts, os.getpid(), log_level, msg)
                self._output(msg)
                # TODO(niklas9):
                # * figure out why task_done() is called too many times at
                #   certain test runs.. and raises ValueError
                try:
                    self.queue.task_done()
                except ValueError:
                    pass

    def _wait_until_queue_is_empty(self):
        # TODO(niklas9):
        # * best practice to exit with some error code 1 if timeout exceeded ?
        total_time_waited = 0
        while not self.queue.empty():
            total_time_waited += self.LOG_FLUSH_TIMEOUT_CHECK
            if total_time_waited == self.LOG_FLUSH_TIMEOUT_WARN:
                msg = ('log queue size is still %d, waiting %d '
                       'more secs for log queue to be flushed..\n'
                       % (self.queue.qsize(), self.LOG_FLUSH_TIMEOUT))
                self._output(msg)
            time.sleep(self.LOG_FLUSH_TIMEOUT_CHECK)
            if total_time_waited >= self.LOG_FLUSH_TIMEOUT:
                msg = ('log timeout reached (%ds), exiting even though '
                       'there are still %d log entries left to be synced\n'
                       % (self.LOG_FLUSH_TIMEOUT, self.queue.qsize()))
                self._output(msg)
                break
        if self.log_fh is not None:
            self.log_fh.close()
