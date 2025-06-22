from gpiozero import OutputDevice


# Class in charge of setting to HIGH the value of the Pin of a transistor
class Transitor(OutputDevice):
    def __init__(self, pin=None, active_high=True):
        super(Transitor, self).__init__(pin, active_high=active_high)
