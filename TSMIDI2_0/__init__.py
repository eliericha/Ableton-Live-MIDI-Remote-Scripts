# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

# import Live
from TSMIDI20Impl import TSMIDIClass


def create_instance(c_instance):
    ' Creates and returns the APC20 script '
    return TSMIDIClass(c_instance)


# local variables:
# tab-width: 4
