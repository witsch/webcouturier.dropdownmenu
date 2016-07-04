# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry


def upgrade_1012_to_1030(context):
    """Upgrade to version 3.0"""

    # PORTAL PROPERTIES
    pprops = getToolByName(context, 'portal_properties')
    if 'dropdown_properties' in pprops:
        pprops.manage_delObjects(['dropdown_properties'])

    # PORTAL SKINS
    pskin = getToolByName(context, 'portal_skins')
    for name, layers in pskin.getSkinPaths():
        layers = layers.split(',')
        if 'dropdownmenu_sunburst' in layers:
            layers.remove('dropdownmenu_sunburst')
        if 'dropdownmenu' in layers:
            layers.remove('dropdownmenu')
        pskin._getSelections()[name] = ','.join(layers)

    if 'dropdownmenu' in pskin:
        pskin.manage_delObjects(['dropdownmenu'])
    if 'dropdownmenu_sunburst' in pskin:
        pskin.manage_delObjects(['dropdownmenu_sunburst'])

    # REGISTRY
    # pre-release cleanup
    registry = getUtility(IRegistry)
    regkey_enable_thumbs = 'webcouturier.dropdownmenu.browser.interfaces.IDropdownConfiguration.enable_thumbs'  # noqa
    if regkey_enable_thumbs in registry.records:
        del registry.records[regkey_enable_thumbs]
