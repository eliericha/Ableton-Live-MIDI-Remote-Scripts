# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

import Live
from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement

class SpecialSessionComponent(SessionComponent):
    " Special SessionComponent for APC combination mode and button to fire selected clip slot "

    def __init__(self, num_tracks, num_scenes):
        SessionComponent.__init__(self, num_tracks, num_scenes)
        self._slot_launch_button = None
        self._play_rec_handlers = []


    def disconnect(self):
        SessionComponent.disconnect(self)
        if (self._slot_launch_button != None):
            self._slot_launch_button.remove_value_listener(self._slot_launch_value)
            self._slot_launch_button = None
        for h in self._play_rec_handlers:
            h.disconnect()


    def link_with_track_offset(self, track_offset, scene_offset):
        assert (track_offset >= 0)
        assert (scene_offset >= 0)
        if self._is_linked():
            self._unlink()
        self.set_offsets(track_offset, scene_offset)
        self._link()


    def unlink(self):
        if self._is_linked():
            self._unlink()


    def set_slot_launch_button(self, button):
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._slot_launch_button != button):
            if (self._slot_launch_button != None):
                self._slot_launch_button.remove_value_listener(self._slot_launch_value)
            self._slot_launch_button = button
            if (self._slot_launch_button != None):
                self._slot_launch_button.add_value_listener(self._slot_launch_value)

            self.update()

    def _slot_launch_value(self, value):
        assert (value in range(128))
        assert (self._slot_launch_button != None)
        if self.is_enabled():
            if ((value != 0) or (not self._slot_launch_button.is_momentary())):
                if (self.song().view.highlighted_clip_slot != None):
                    self.song().view.highlighted_clip_slot.fire()

    def set_clip_play_or_rec(self, control_surface, clip_slot_component, button):
        self._play_rec_handlers.append(ClipPlayOrRecHandler(control_surface, clip_slot_component, button))


class ClipPlayOrRecHandler(object):

    def __init__(self, control_surface, clip_slot_component, button):
        self._control_surface = control_surface
        self._clip_slot_component = clip_slot_component
        self._button = button
        self.connect()

    def connect(self):
        self._control_surface.log_message("Connecting button %s to clip slot %s" % (self._button, self._clip_slot_component.name))
        self._button.add_value_listener(self._clip_play_or_rec_listener)

    def disconnect(self):
        self._control_surface.log_message("Disconnecting button %s from clip slot %s" % (self._button, self._clip_slot_component.name))
        self._button.remove_value_listener(self._clip_play_or_rec_listener)

    def _clip_play_or_rec_listener(self, value):
        # self._control_surface.log_message("_clip_play_or_rec called with value: %d" % value)
        if value:
            clip_slot = self._clip_slot_component._clip_slot
            if clip_slot:
                # self._control_surface.log_message("clip_slot:\n%s" % dir(clip_slot))
                if not clip_slot.has_clip:
                    parent_track = clip_slot.canonical_parent
                    if parent_track and parent_track.can_be_armed:
                        parent_track.arm = True
                        clip_slot.fire()