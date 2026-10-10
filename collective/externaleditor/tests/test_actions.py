from collective.externaleditor.interfaces import IExternalEditorLayer
from collective.externaleditor.testing import (  # noqa: E501
    COLLECTIVE_EXTERNALEDITOR_FUNCTIONAL_TESTING,
)
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.interface import alsoProvides

import unittest


PLONE_EXPR = "object/externalEditorEnabled|nothing"


class TestExteditAction(unittest.TestCase):
    layer = COLLECTIVE_EXTERNALEDITOR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        alsoProvides(self.layer["request"], IExternalEditorLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        member = self.portal.portal_membership.getAuthenticatedMember()
        member.setMemberProperties({"ext_editor": True})
        self.action = self.portal.portal_actions.document_actions.extedit

    def listed(self, obj):
        actions = self.portal.portal_actions.listFilteredActionsFor(obj)
        return "extedit" in [a["id"] for a in actions.get("document_actions", [])]

    def available(self, obj):
        return obj.restrictedTraverse("@@externalEditorEnabled").available()

    def test_listed_only_when_available(self):
        self.portal.invokeFactory("File", "file")
        self.portal.invokeFactory("Folder", "folder")
        self.assertTrue(self.available(self.portal.file))
        self.assertTrue(self.listed(self.portal.file))
        self.assertFalse(self.available(self.portal.folder))
        self.assertFalse(self.listed(self.portal.folder))

    def test_uninstall(self):
        applyProfile(self.portal, "collective.externaleditor:uninstall")
        self.assertEqual(self.action.available_expr, PLONE_EXPR)

    def test_upgrade(self):
        self.action._setPropValue("available_expr", PLONE_EXPR)
        setup = self.portal.portal_setup
        setup.setLastVersionForProfile("collective.externaleditor:default", "1001")
        setup.upgradeProfile("collective.externaleditor:default")
        self.assertEqual(
            self.action.available_expr, "object/@@externalEditorEnabled/available"
        )
