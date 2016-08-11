import time
import datetime
import pytest
import os

def test_almafa():
    try:
        os.remove("/tmp/bbb.txt")
    except:
        pass
    for i in range(1, 10):
        time.sleep(1)
        with open("/tmp/bbb.txt", 'a') as fileobj:
            fileobj.write("fileb before state :%s\n" % pytest.state)
            pytest.state = "b%s" % str(datetime.datetime.now())
            fileobj.write("fileb after  state :%s\n" % pytest.state)
        print("testb: %s " % i)
        assert "AAA" == "AAA"
