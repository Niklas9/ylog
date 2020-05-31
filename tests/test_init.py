
import nose

import ylog


class TestLog(object):

    @nose.tools.raises(ylog.InvalidLogLevelException)
    def test_invalid_log_level(self):
        ylog.Log(log_level=3, re_init=True)

    def test_singleton_of_log_class(self):
        l1 = ylog.Log()
        l2 = ylog.Log()
        assert id(l1) == id(l2)
