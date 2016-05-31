# -*- coding: utf-8 -*-
from plone import api

_WC = 'webcouturier.dropdownmenu.browser.interfaces.IDropdownConfiguration.{0}'


def _get_cfg(name):
    return api.portal.get_registry_record(_WC.format(name))


def getDropdownDepth():
    return _get_cfg('dropdown_depth')


def cachingEnabled():
    return _get_cfg('enable_caching')


def parentClickable():
    return _get_cfg('enable_parent_clickable')


def enableImages():
    return _get_cfg('enable_images')


def imgSize():
    return _get_cfg('img_size')


def enableDesc():
    return _get_cfg('enable_desc')
