from Products.CMFCore.interfaces import IPropertiesTool
from zope.component import getUtility


def getDropdownDepth():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('dropdown_depth')


def cachingEnabled():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('enable_caching', False)


def parentClickable():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('enable_parent_clickable', True)

def enableThumbs():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('enable_thumbs', True)
    
def enableDesc():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('enable_desc', True)

