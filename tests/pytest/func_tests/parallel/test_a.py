import time
import datetime
import pytest
import os

def test_almafa():
    time.sleep(0.5)
    try:
        os.remove("/tmp/aaa.txt")
    except:
        pass
    for i in range(1, 10):
        time.sleep(1)
        with open("/tmp/aaa.txt", 'a') as fileobj:
            fileobj.write("filea before state :%s\n" % pytest.state)
            pytest.state = "a%s" % str(datetime.datetime.now())
            fileobj.write("filea after  state :%s\n" % pytest.state)
        # print(datetime.datetime.now())
        print("testa: %s " % i)
        assert "AAA" == "AAA"
