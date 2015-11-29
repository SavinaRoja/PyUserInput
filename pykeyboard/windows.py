#Copyright 2013 Paul Barton
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ctypes import *
import win32api
from win32con import *
import pythoncom

from .base import PyKeyboardMeta, PyKeyboardEventMeta

import time


class SupportError(Exception):
    """For keys not supported on this system"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return('The {0} key is not supported in Windows'.format(self.value))


class PyKeyboard(PyKeyboardMeta):
    """
    The PyKeyboard implementation for Windows systems. This allows one to
    simulate keyboard input.
    """
    def __init__(self):
        PyKeyboardMeta.__init__(self)
        self.special_key_assignment()

    def press_key(self, character=''):
        """
        Press a given character key.
        """
        try:
            shifted = self.is_char_shifted(character)
        except AttributeError:
            win32api.keybd_event(character, 0, 0, 0)
        else:
            if shifted:
                win32api.keybd_event(self.shift_key, 0, 0, 0)
            char_vk = win32api.VkKeyScan(character)
            win32api.keybd_event(char_vk, 0, 0, 0)

    def release_key(self, character=''):
        """
        Release a given character key.
        """
        try:
            shifted = self.is_char_shifted(character)
        except AttributeError:
            win32api.keybd_event(character, 0, KEYEVENTF_KEYUP, 0)
        else:
            if shifted:
                win32api.keybd_event(self.shift_key, 0, KEYEVENTF_KEYUP, 0)
            char_vk = win32api.VkKeyScan(character)
            win32api.keybd_event(char_vk, 0, KEYEVENTF_KEYUP, 0)

    def special_key_assignment(self):
        """
        Special Key assignment for windows
        """
        #As defined by Microsoft, refer to:
        #http://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx
        self.backspace_key = VK_BACK
        self.tab_key = VK_TAB
        self.clear_key = VK_CLEAR
        self.return_key = VK_RETURN
        self.enter_key = self.return_key  # Because many keyboards call it "Enter"
        self.shift_key = VK_SHIFT
        self.shift_l_key = VK_LSHIFT
        self.shift_r_key = VK_RSHIFT
        self.control_key = VK_CONTROL
        self.control_l_key = VK_LCONTROL
        self.control_r_key = VK_RCONTROL
        #Windows uses "menu" to refer to Alt...
        self.menu_key = VK_MENU
        self.alt_l_key = VK_LMENU
        self.alt_r_key = VK_RMENU
        self.altgr_key = VK_RMENU
        self.alt_key = self.alt_l_key
        self.pause_key = VK_PAUSE
        self.caps_lock_key = VK_CAPITAL
        self.capital_key = self.caps_lock_key
        self.num_lock_key = VK_NUMLOCK
        self.scroll_lock_key = VK_SCROLL
        #Windows Language Keys,
        self.kana_key = VK_KANA
        self.hangeul_key = VK_HANGEUL # old name - should be here for compatibility
        self.hangul_key = VK_HANGUL
        self.junjua_key = VK_JUNJA
        self.final_key = VK_FINAL
        self.hanja_key = VK_HANJA
        self.kanji_key = VK_KANJI
        self.convert_key = VK_CONVERT
        self.nonconvert_key = VK_NONCONVERT
        self.accept_key = VK_ACCEPT
        self.modechange_key = VK_MODECHANGE
        #More Keys
        self.escape_key = VK_ESCAPE
        self.space_key = VK_SPACE
        self.prior_key = VK_PRIOR
        self.next_key = VK_NEXT
        self.page_up_key = self.prior_key
        self.page_down_key = self.next_key
        self.home_key = VK_HOME
        self.up_key = VK_UP
        self.down_key = VK_DOWN
        self.left_key = VK_LEFT
        self.right_key = VK_RIGHT
        self.end_key = VK_END
        self.select_key = VK_SELECT
        self.print_key = VK_PRINT
        self.snapshot_key = VK_SNAPSHOT
        self.print_screen_key = self.snapshot_key
        self.execute_key = VK_EXECUTE
        self.insert_key = VK_INSERT
        self.delete_key = VK_DELETE
        self.help_key = VK_HELP
        self.windows_l_key = VK_LWIN
        self.super_l_key = self.windows_l_key
        self.windows_r_key = VK_RWIN
        self.super_r_key = self.windows_r_key
        self.apps_key = VK_APPS
        #Numpad
        self.keypad_keys = {'Space': None,
                            'Tab': None,
                            'Enter': None,  # Needs Fixing
                            'F1': None,
                            'F2': None,
                            'F3': None,
                            'F4': None,
                            'Home': VK_NUMPAD7,
                            'Left': VK_NUMPAD4,
                            'Up': VK_NUMPAD8,
                            'Right': VK_NUMPAD6,
                            'Down': VK_NUMPAD2,
                            'Prior': None,
                            'Page_Up': VK_NUMPAD9,
                            'Next': None,
                            'Page_Down': VK_NUMPAD3,
                            'End': VK_NUMPAD1,
                            'Begin': None,
                            'Insert': VK_NUMPAD0,
                            'Delete': VK_DECIMAL,
                            'Equal': None,  # Needs Fixing
                            'Multiply': VK_MULTIPLY,
                            'Add': VK_ADD,
                            'Separator': VK_SEPARATOR,
                            'Subtract': VK_SUBTRACT,
                            'Decimal': VK_DECIMAL,
                            'Divide': VK_DIVIDE,
                            0: VK_NUMPAD0,
                            1: VK_NUMPAD1,
                            2: VK_NUMPAD2,
                            3: VK_NUMPAD3,
                            4: VK_NUMPAD4,
                            5: VK_NUMPAD5,
                            6: VK_NUMPAD6,
                            7: VK_NUMPAD7,
                            8: VK_NUMPAD8,
                            9: VK_NUMPAD9}
        self.numpad_keys = self.keypad_keys
        #FKeys
        self.function_keys = [None, VK_F1, VK_F2, VK_F3, VK_F4, VK_F5, VK_F6,
                              VK_F7, VK_F8, VK_F9, VK_F10, VK_F11, VK_F12,
                              VK_F13, VK_F14, VK_F15, VK_F16, VK_F17, VK_F18,
                              VK_F19, VK_F20, VK_F21, VK_F22, VK_F23, VK_F24,
                              None, None, None, None, None, None, None, None,
                              None, None, None]  # Up to 36 as in x11
        #Miscellaneous
        self.cancel_key = VK_CANCEL
        self.break_key = self.cancel_key
        self.mode_switch_key = VK_MODECHANGE
        self.browser_back_key = VK_BROWSER_BACK
        self.browser_forward_key = VK_BROWSER_FORWARD
        self.processkey_key = VK_PROCESSKEY
        self.attn_key = VK_ATTN
        self.crsel_key = VK_CRSEL
        self.exsel_key = VK_EXSEL
        self.ereof_key = VK_EREOF
        self.play_key = VK_PLAY
        self.zoom_key = VK_ZOOM
        self.noname_key = VK_NONAME
        self.pa1_key = VK_PA1
        self.oem_clear_key = VK_OEM_CLEAR
        self.volume_mute_key = VK_VOLUME_MUTE
        self.volume_down_key = VK_VOLUME_DOWN
        self.volume_up_key = VK_VOLUME_UP
        self.media_next_track_key = VK_MEDIA_NEXT_TRACK
        self.media_prev_track_key = VK_MEDIA_PREV_TRACK
        self.media_play_pause_key = VK_MEDIA_PLAY_PAUSE
        self.begin_key = self.home_key
        #LKeys - Unsupported
        self.l_keys = [None] * 11
        #RKeys - Unsupported
        self.r_keys = [None] * 16

        #Other unsupported Keys from X11
        self.linefeed_key = None
        self.find_key = None
        self.meta_l_key = None
        self.meta_r_key = None
        self.sys_req_key = None
        self.hyper_l_key = None
        self.hyper_r_key = None
        self.undo_key = None
        self.redo_key = None
        self.script_switch_key = None

class PyKeyboardEvent(PyKeyboardEventMeta):
    """
    The PyKeyboardEvent implementation for Windows Systems. This allows one
    to listen for keyboard input.
    """
    def __init__(self, diagnostic=False):
        self.diagnostic = diagnostic

        import pyHook

        PyKeyboardEventMeta.__init__(self)
        self.hm = pyHook.HookManager()
        self.hc = pyHook.HookConstants()

        self.lock_meaning = None

    def run(self):
        """Begin listening for keyboard input events."""
        self.state = True
        self.hm.KeyAll = self.handler
        self.hm.HookKeyboard()
        while self.state:
            time.sleep(0.01)
            pythoncom.PumpWaitingMessages()

    def stop(self):
        """Stop listening for keyboard input events."""
        self.hm.UnhookKeyboard()
        self.state = False

    def handler(self, event):
        """Upper level handler of keyboard events."""

        if self.escape(event):  # A chance to escape
            self.stop()
        elif self.diagnostic:
            self._diagnostic(event)
        else:
            self._tap(event)
        #This is needed according to the pyHook tutorials 'http://sourceforge.net/apps/mediawiki/pyhook/index.php?title=PyHook_Tutorial'
        return True

    def _tap(self, event):
        keycode = event.KeyID
        press_bool = (event.Message in [self.hc.WM_KEYDOWN, self.hc.WM_SYSKEYDOWN])

        #Not using event.GeyKey() because we want to differentiate between
        #KeyID and Ascii attributes of the event
        if event.Ascii != 0:
            character = chr(event.Ascii)
        else:
            character = self.hc.id_to_vk[keycode][3:]

        #TODO: Need to universalize keys between platforms. ie. 'Menu' -> 'Alt'

        self.tap(keycode, character, press_bool)

    def _diagnostic(self, event):
        """
        This method is employed instead of _tap() if the PyKeyboardEvent is
        initialized with diagnostic=True. This makes some basic testing quickly
        and easily available. It will print out information regarding the event
        instead of passing information along to self.tap()
        """
        print('\n---Keyboard Event Diagnostic---')
        print('MessageName:', event.MessageName)
        print('Message:', event.Message)
        print('Time:', event.Time)
        print('Window:', event.Window)
        print('WindowName:', event.WindowName)
        print('Ascii:', event.Ascii, ',', chr(event.Ascii))
        print('Key:', event.Key)
        print('KeyID:', event.KeyID)
        print('ScanCode:', event.ScanCode)
        print('Extended:', event.Extended)
        print('Injected:', event.Injected)
        print('Alt', event.Alt)
        print('Transition', event.Transition)
        print('---')

    def escape(self, event):
        return event.KeyID == VK_ESCAPE

    def toggle_shift_state(self):  # This will be removed later
        '''Does toggling for the shift state.'''
        states = [1, 0]
        self.shift_state = states[self.shift_state]

    def toggle_alt_state(self):  # This will be removed later
        '''Does toggling for the alt state.'''
        states = [2, None, 0]
        self.alt_state = states[self.alt_state]

    def configure_keys(self):
        """
        This does initial configuration for keyboard modifier state tracking
        including alias setting and keycode list construction.
        """
        pass
