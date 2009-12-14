
from zope.interface import Interface
from zope.schema import List
from zope.schema import Dict


class ILayoutRegistry(Interface):
    """ """

    layouts = List(
        title=u"Layouts list",
        default=['main_layout'])
    
    assigments = Dict(
        title=u"Layout assigments",
        default=dict())


