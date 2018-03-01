# -*- coding: utf-8 -*-
"""Setup tests for webcouturier.dropdownmenu."""
from plone import api
from plone.browserlayer import utils
from webcouturier.dropdownmenu.browser.interfaces import IDropdownSpecific
from webcouturier.dropdownmenu.testing import DROPDOWN_CONTENT_INTEGRATION_TESTING  # noqa E501

import unittest


class TestSetup(unittest.TestCase):
    """Test that webcouturier.dropdownmenu is properly installed."""

    layer = DROPDOWN_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Setting up Testcase."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if webcouturier.dropdownmenu is installed."""
        self.assertTrue(
            self.installer.isProductInstalled(
                'webcouturier.dropdownmenu',
            ),
        )

    def test_browserlayer(self):
        """Test that IDropdownSpecific is registered."""
        from plone.browserlayer import utils
        self.assertIn(
            IDropdownSpecific,
            utils.registered_layers(),
        )


class TestUninstall(unittest.TestCase):
    """Uninstall Routine."""

    layer = DROPDOWN_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Setting up Testcase."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['webcouturier.dropdownmenu'])

    def test_product_uninstalled(self):
        """Test if webcouturier.dropdownmenu is cleanly uninstalled."""
        self.assertFalse(
            self.installer.isProductInstalled(
                'webcouturier.dropdownmenu',
            ),
        )

    def test_browserlayer_removed(self):
        """Test that IDropdownSpecific is removed."""
        self.assertNotIn(
            IDropdownSpecific,
            utils.registered_layers(),
        )
