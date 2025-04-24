import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/nicholas/arduinobot_ws/install/arduinobot_py_examples'
