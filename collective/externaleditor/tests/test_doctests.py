from collective.externaleditor.testing import COLLECTIVE_EXTERNALEDITOR_FUNCTIONAL_TESTING  # noqa: E501
from plone.testing import layered
from unittest import TestSuite

import doctest


OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE



def test_suite():
    return TestSuite(
        [
            layered(
                doctest.DocFileSuite(ft, optionflags=OPTIONFLAGS,),
                layer=COLLECTIVE_EXTERNALEDITOR_FUNCTIONAL_TESTING,
            )
            for ft in ["controlpanel.txt"]
        ]
    )
