# -*- coding: utf-8 -*-
from Products.CMFCore.interfaces import IPropertiesTool
from zope.component import getUtility


def getDropdownDepth():
    return api.portal.get_registry_record('webcouturier.dropdownmenu.browser.interfaces.IDropdownConfiguration.dropdown_depth')


def cachingEnabled():
    return api.portal.get_registry_record('webcouturier.dropdownmenu.browser.interfaces.IDropdownConfiguration.enable_caching')


def parentClickable():
    return api.portal.get_registry_record('webcouturier.dropdownmenu.browser.interfaces.IDropdownConfiguration.enable_parent_clickable')


def enableThumbs():
    return api.portal.get_registry_record('webcouturier.dropdownmenu.browser.interfaces.IDropdownConfiguration.enable_thumbs')


def enableDesc():
    return api.portal.get_registry_record('webcouturier.dropdownmenu.browser.interfaces.IDropdownConfiguration.enable_desc')
