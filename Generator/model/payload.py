import model.message
import property
import logging
import utils
from common import *

class Payload(Message):
    def __init__(self, namespace, name, tag, isAbstract):
        super(Payload, self).__init__(namespace, name)
        self.objectType = ObjectType.Payload
