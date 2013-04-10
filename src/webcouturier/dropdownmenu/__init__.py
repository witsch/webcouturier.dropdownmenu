from AccessControl import allow_module
from zope.i18nmessageid import MessageFactory

msg_fact = MessageFactory('webcouturier.dropdownmenu')
allow_module('webcouturier.dropdownmenu.utils')
