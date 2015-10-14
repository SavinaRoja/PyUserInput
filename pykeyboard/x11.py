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

from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
from Xlib.ext import record
from Xlib.protocol import rq
import Xlib.XK
import Xlib.keysymdef.xkb

from .base import PyKeyboardMeta, PyKeyboardEventMeta

import time
import string

from pymouse.x11 import display_manager

from .x11_keysyms import KEYSYMS


class PyKeyboard(PyKeyboardMeta):
    """
    The PyKeyboard implementation for X11 systems (mostly linux). This
    allows one to simulate keyboard input.
    """
    def __init__(self, display=None):
        PyKeyboardMeta.__init__(self)
        self.display = Display(display)
        self.display2 = Display(display)
        self.special_key_assignment()

    def _handle_key(self, character, event):
        """Handles either a key press or release, depending on ``event``.

        :param character: The key to handle. See :meth:`press_key` and
        :meth:`release_key` for information about this parameter.

        :param event: The *Xlib* event. This should be either
        :attr:`Xlib.X.KeyPress` or :attr:`Xlib.X.KeyRelease`
        """
        try:
            # Detect uppercase or shifted character
            shifted = self.is_char_shifted(character)
        except AttributeError:
            # Handle the case of integer keycode argument
            with display_manager(self.display) as d:
                fake_input(d, event, character)
        else:
            with display_manager(self.display) as d:
                if shifted:
                    fake_input(d, event, self.shift_key)
                keycode = self.lookup_character_keycode(character)
                fake_input(d, event, keycode)

    def press_key(self, character=''):
        """
        Press a given character key. Also works with character keycodes as
        integers, but not keysyms.
        """
        self._handle_key(character, X.KeyPress)

    def release_key(self, character=''):
        """
        Release a given character key. Also works with character keycodes as
        integers, but not keysyms.
        """
        self._handle_key(character, X.KeyRelease)

    def special_key_assignment(self):
        """
        Determines the keycodes for common special keys on the keyboard. These
        are integer values and can be passed to the other key methods.
        Generally speaking, these are non-printable codes.
        """
        #This set of keys compiled using the X11 keysymdef.h file as reference
        #They comprise a relatively universal set of keys, though there may be
        #exceptions which may come up for other OSes and vendors. Countless
        #special cases exist which are not handled here, but may be extended.
        #TTY Function Keys
        self.backspace_key = self.lookup_character_keycode('BackSpace')
        self.tab_key = self.lookup_character_keycode('Tab')
        self.linefeed_key = self.lookup_character_keycode('Linefeed')
        self.clear_key = self.lookup_character_keycode('Clear')
        self.return_key = self.lookup_character_keycode('Return')
        self.enter_key = self.return_key  # Because many keyboards call it "Enter"
        self.pause_key = self.lookup_character_keycode('Pause')
        self.scroll_lock_key = self.lookup_character_keycode('Scroll_Lock')
        self.sys_req_key = self.lookup_character_keycode('Sys_Req')
        self.escape_key = self.lookup_character_keycode('Escape')
        self.delete_key = self.lookup_character_keycode('Delete')
        #Modifier Keys
        self.shift_l_key = self.lookup_character_keycode('Shift_L')
        self.shift_r_key = self.lookup_character_keycode('Shift_R')
        self.shift_key = self.shift_l_key  # Default Shift is left Shift
        self.alt_l_key = self.lookup_character_keycode('Alt_L')
        self.alt_r_key = self.lookup_character_keycode('Alt_R')
        self.altgr_key = self.lookup_character_keycode('ISO_Level3_Shift')
        self.alt_key = self.alt_l_key  # Default Alt is left Alt
        self.control_l_key = self.lookup_character_keycode('Control_L')
        self.control_r_key = self.lookup_character_keycode('Control_R')
        self.control_key = self.control_l_key  # Default Ctrl is left Ctrl
        self.caps_lock_key = self.lookup_character_keycode('Caps_Lock')
        self.capital_key = self.caps_lock_key  # Some may know it as Capital
        self.shift_lock_key = self.lookup_character_keycode('Shift_Lock')
        self.meta_l_key = self.lookup_character_keycode('Meta_L')
        self.meta_r_key = self.lookup_character_keycode('Meta_R')
        self.super_l_key = self.lookup_character_keycode('Super_L')
        self.windows_l_key = self.super_l_key  # Cross-support; also it's printed there
        self.super_r_key = self.lookup_character_keycode('Super_R')
        self.windows_r_key = self.super_r_key  # Cross-support; also it's printed there
        self.hyper_l_key = self.lookup_character_keycode('Hyper_L')
        self.hyper_r_key = self.lookup_character_keycode('Hyper_R')
        #Cursor Control and Motion
        self.home_key = self.lookup_character_keycode('Home')
        self.up_key = self.lookup_character_keycode('Up')
        self.down_key = self.lookup_character_keycode('Down')
        self.left_key = self.lookup_character_keycode('Left')
        self.right_key = self.lookup_character_keycode('Right')
        self.end_key = self.lookup_character_keycode('End')
        self.begin_key = self.lookup_character_keycode('Begin')
        self.page_up_key = self.lookup_character_keycode('Page_Up')
        self.page_down_key = self.lookup_character_keycode('Page_Down')
        self.prior_key = self.lookup_character_keycode('Prior')
        self.next_key = self.lookup_character_keycode('Next')
        #Misc Functions
        self.select_key = self.lookup_character_keycode('Select')
        self.print_key = self.lookup_character_keycode('Print')
        self.print_screen_key = self.print_key  # Seems to be the same thing
        self.snapshot_key = self.print_key  # Another name for printscreen
        self.execute_key = self.lookup_character_keycode('Execute')
        self.insert_key = self.lookup_character_keycode('Insert')
        self.undo_key = self.lookup_character_keycode('Undo')
        self.redo_key = self.lookup_character_keycode('Redo')
        self.menu_key = self.lookup_character_keycode('Menu')
        self.apps_key = self.menu_key  # Windows...
        self.find_key = self.lookup_character_keycode('Find')
        self.cancel_key = self.lookup_character_keycode('Cancel')
        self.help_key = self.lookup_character_keycode('Help')
        self.break_key = self.lookup_character_keycode('Break')
        self.mode_switch_key = self.lookup_character_keycode('Mode_switch')
        self.script_switch_key = self.lookup_character_keycode('script_switch')
        self.num_lock_key = self.lookup_character_keycode('Num_Lock')
        #Keypad Keys: Dictionary structure
        keypad = ['Space', 'Tab', 'Enter', 'F1', 'F2', 'F3', 'F4', 'Home',
                  'Left', 'Up', 'Right', 'Down', 'Prior', 'Page_Up', 'Next',
                  'Page_Down', 'End', 'Begin', 'Insert', 'Delete', 'Equal',
                  'Multiply', 'Add', 'Separator', 'Subtract', 'Decimal',
                  'Divide', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.keypad_keys = dict((k, self.lookup_character_keycode('KP_'+str(k))) for k in keypad)
        self.numpad_keys = self.keypad_keys
        #Function Keys/ Auxilliary Keys
        #FKeys
        self.function_keys = [None] + [self.lookup_character_keycode('F'+str(i)) for i in range(1,36)]
        #LKeys
        self.l_keys = [None] + [self.lookup_character_keycode('L'+str(i)) for i in range(1,11)]
        #RKeys
        self.r_keys = [None] + [self.lookup_character_keycode('R'+str(i)) for i in range(1,16)]

        #Unsupported keys from windows
        self.kana_key = None
        self.hangeul_key = None # old name - should be here for compatibility
        self.hangul_key = None
        self.junjua_key = None
        self.final_key = None
        self.hanja_key = None
        self.kanji_key = None
        self.convert_key = None
        self.nonconvert_key = None
        self.accept_key = None
        self.modechange_key = None
        self.sleep_key = None

    def lookup_character_keycode(self, character):
        """
        Looks up the keysym for the character then returns the keycode mapping
        for that keysym.
        """
        keysym = Xlib.XK.string_to_keysym(character)
        if not keysym:
            try:
                keysym = getattr(Xlib.keysymdef.xkb, 'XK_' + character, 0)
            except:
                keysym = 0
        if not keysym:
            keysym = Xlib.XK.string_to_keysym(KEYSYMS[character])
        return self.display.keysym_to_keycode(keysym)


class PyKeyboardEvent(PyKeyboardEventMeta):
    """
    The PyKeyboardEvent implementation for X11 systems (mostly linux). This
    allows one to listen for keyboard input.
    """
    def __init__(self, capture=False, display=None):
        self.display = Display(display)
        self.display2 = Display(display)
        self.ctx = self.display2.record_create_context(
            0,
            [record.AllClients],
            [{
                    'core_requests': (0, 0),
                    'core_replies': (0, 0),
                    'ext_requests': (0, 0, 0, 0),
                    'ext_replies': (0, 0, 0, 0),
                    'delivered_events': (0, 0),
                    'device_events': (X.KeyPress, X.KeyRelease),
                    'errors': (0, 0),
                    'client_started': False,
                    'client_died': False,
            }])

        self.lock_meaning = None

        #Get these dictionaries for converting keysyms and strings
        self.keysym_to_string, self.string_to_keysym = self.get_translation_dicts()

        #Identify and register special groups of keys
        self.modifier_keycodes = {}
        self.all_mod_keycodes = []
        self.keypad_keycodes = []
        #self.configure_keys()

        #Direct access to the display's keycode-to-keysym array
        #print('Keycode to Keysym map')
        #for i in range(len(self.display._keymap_codes)):
        #    print('{0}: {1}'.format(i, self.display._keymap_codes[i]))

        PyKeyboardEventMeta.__init__(self, capture)

    def run(self):
        """Begin listening for keyboard input events."""
        self.state = True
        if self.capture:
            self.display2.screen().root.grab_keyboard(X.KeyPressMask | X.KeyReleaseMask, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)

        self.display2.record_enable_context(self.ctx, self.handler)
        self.display2.record_free_context(self.ctx)

    def stop(self):
        """Stop listening for keyboard input events."""
        self.state = False
        with display_manager(self.display) as d:
            d.record_disable_context(self.ctx)
            d.ungrab_keyboard(X.CurrentTime)
        with display_manager(self.display2):
            d.record_disable_context(self.ctx)
            d.ungrab_keyboard(X.CurrentTime)

    def handler(self, reply):
        """Upper level handler of keyboard events."""
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self.display.display, None, None)
            if self.escape(event):  # Quit if this returns True
                self.stop()
            else:
                self._tap(event)

    def _tap(self, event):
        keycode = event.detail
        press_bool = (event.type == X.KeyPress)

        #Detect modifier states from event.state
        for mod, bit in self.modifier_bits.items():
            self.modifiers[mod] = event.state & bit

        if keycode in self.all_mod_keycodes:
            keysym = self.display.keycode_to_keysym(keycode, 0)
            character = self.keysym_to_string[keysym]
        else:
            character = self.lookup_char_from_keycode(keycode)

        #All key events get passed to self.tap()
        self.tap(keycode,
                 character,
                 press=press_bool)

    def lookup_char_from_keycode(self, keycode):
        """
        This will conduct a lookup of the character or string associated with a
        given keycode.
        """

        #TODO: Logic should be strictly adapted from X11's src/KeyBind.c
        #Right now the logic is based off of
        #http://tronche.com/gui/x/xlib/input/keyboard-encoding.html
        #Which I suspect is not the whole story and may likely cause bugs

        keysym_index = 0
        #TODO: Display's Keysyms per keycode count? Do I need this?
        #If the Num_Lock is on, and the keycode corresponds to the keypad
        if self.modifiers['Num_Lock'] and keycode in self.keypad_keycodes:
            if self.modifiers['Shift'] or self.modifiers['Shift_Lock']:
                keysym_index = 0
            else:
                keysym_index = 1

        elif not self.modifiers['Shift'] and self.modifiers['Caps_Lock']:
            #Use the first keysym if uppercase or uncased
            #Use the uppercase keysym if the first is lowercase (second)
            keysym_index = 0
            keysym = self.display.keycode_to_keysym(keycode, keysym_index)
            #TODO: Support Unicode, Greek, and special latin characters
            if keysym & 0x7f == keysym and chr(keysym) in 'abcdefghijklmnopqrstuvwxyz':
                keysym_index = 1

        elif self.modifiers['Shift'] and self.modifiers['Caps_Lock']:
            keysym_index = 1
            keysym = self.display.keycode_to_keysym(keycode, keysym_index)
            #TODO: Support Unicode, Greek, and special latin characters
            if keysym & 0x7f == keysym and chr(keysym) in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                keysym_index = 0

        elif self.modifiers['Shift'] or self.modifiers['Shift_Lock']:
            keysym_index = 1

        if self.modifiers['Mode_switch']:
            keysym_index += 2

        #Finally! Get the keysym
        keysym = self.display.keycode_to_keysym(keycode, keysym_index)

        #If the character is ascii printable, return that character
        if keysym & 0x7f == keysym and self.ascii_printable(keysym):
            return chr(keysym)

        #If the character was not printable, look for its name
        try:
            char = self.keysym_to_string[keysym]
        except KeyError:
            print('Unable to determine character.')
            print('Keycode: {0} KeySym {1}'.format(keycode, keysym))
            return None
        else:
            return char

    def escape(self, event):
        if event.detail == self.lookup_character_keycode('Escape'):
            return True
        return False

    def configure_keys(self):
        """
        This function locates the keycodes corresponding to special groups of
        keys and creates data structures of them for use by the PyKeyboardEvent
        instance; including the keypad keys and the modifiers.

        The keycodes pertaining to the keyboard modifiers are assigned by the
        modifier name in a dictionary. This dictionary can be accessed in the
        following manner:
            self.modifier_keycodes['Shift']  # All keycodes for Shift Masking

        It also assigns certain named modifiers (Alt, Num_Lock, Super), which
        may be dynamically assigned to Mod1 - Mod5 on different platforms. This
        should generally allow the user to do the following lookups on any
        system:
            self.modifier_keycodes['Alt']  # All keycodes for Alt Masking
            self.modifiers['Alt']  # State of Alt mask, non-zero if "ON"
        """
        modifier_mapping = self.display.get_modifier_mapping()
        all_mod_keycodes = []
        mod_keycodes = {}
        mod_index = [('Shift', X.ShiftMapIndex), ('Lock', X.LockMapIndex),
                     ('Control', X.ControlMapIndex), ('Mod1', X.Mod1MapIndex),
                     ('Mod2', X.Mod2MapIndex), ('Mod3', X.Mod3MapIndex),
                     ('Mod4', X.Mod4MapIndex), ('Mod5', X.Mod5MapIndex)]
        #This gets the list of all keycodes per Modifier, assigns to name
        for name, index in mod_index:
            codes = [v for v in list(modifier_mapping[index]) if v]
            mod_keycodes[name] = codes
            all_mod_keycodes += codes

        def lookup_keycode(string):
            keysym = self.string_to_keysym[string]
            return self.display.keysym_to_keycode(keysym)

        #Dynamically assign Lock to Caps_Lock, Shift_Lock, Alt, Num_Lock, Super,
        #and mode switch. Set in both mod_keycodes and self.modifier_bits

        #Try to assign Lock to Caps_Lock or Shift_Lock
        shift_lock_keycode = lookup_keycode('Shift_Lock')
        caps_lock_keycode = lookup_keycode('Caps_Lock')

        if shift_lock_keycode in mod_keycodes['Lock']:
            mod_keycodes['Shift_Lock'] = [shift_lock_keycode]
            self.modifier_bits['Shift_Lock'] = self.modifier_bits['Lock']
            self.lock_meaning = 'Shift_Lock'
        elif caps_lock_keycode in mod_keycodes['Lock']:
            mod_keycodes['Caps_Lock'] = [caps_lock_keycode]
            self.modifier_bits['Caps_Lock'] = self.modifier_bits['Lock']
            self.lock_meaning = 'Caps_Lock'
        else:
            self.lock_meaning = None
        #print('Lock is bound to {0}'.format(self.lock_meaning))

        #Need to find out which Mod# to use for Alt, Num_Lock, Super, and
        #Mode_switch
        num_lock_keycodes = [lookup_keycode('Num_Lock')]
        alt_keycodes = [lookup_keycode(i) for i in ['Alt_L', 'Alt_R']]
        super_keycodes = [lookup_keycode(i) for i in ['Super_L', 'Super_R']]
        mode_switch_keycodes = [lookup_keycode('Mode_switch')]

        #Detect Mod number for Alt, Num_Lock, and Super
        for name, keycodes in list(mod_keycodes.items()):
            for alt_key in alt_keycodes:
                if alt_key in keycodes:
                    mod_keycodes['Alt'] = keycodes
                    self.modifier_bits['Alt'] = self.modifier_bits[name]
            for num_lock_key in num_lock_keycodes:
                if num_lock_key in keycodes:
                    mod_keycodes['Num_Lock'] = keycodes
                    self.modifier_bits['Num_Lock'] = self.modifier_bits[name]
            for super_key in super_keycodes:
                if super_key in keycodes:
                    mod_keycodes['Super'] = keycodes
                    self.modifier_bits['Super'] = self.modifier_bits[name]
            for mode_switch_key in mode_switch_keycodes:
                if mode_switch_key in keycodes:
                    mod_keycodes['Mode_switch'] = keycodes
                    self.modifier_bits['Mode_switch'] = self.modifier_bits[name]

        #Assign the mod_keycodes to a local variable for access
        self.modifier_keycodes = mod_keycodes
        self.all_mod_keycodes = all_mod_keycodes

        #TODO: Determine if this might fail, perhaps iterate through the mapping
        #and identify all keycodes with registered keypad keysyms?

        #Acquire the full list of keypad keycodes
        self.keypad_keycodes = []
        keypad = ['Space', 'Tab', 'Enter', 'F1', 'F2', 'F3', 'F4', 'Home',
                  'Left', 'Up', 'Right', 'Down', 'Prior', 'Page_Up', 'Next',
                  'Page_Down', 'End', 'Begin', 'Insert', 'Delete', 'Equal',
                  'Multiply', 'Add', 'Separator', 'Subtract', 'Decimal',
                  'Divide', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for keyname in keypad:
            keypad_keycode = self.lookup_character_keycode('KP_' + keyname)
            self.keypad_keycodes.append(keypad_keycode)

    def lookup_character_keycode(self, character):
        """
        Looks up the keysym for the character then returns the keycode mapping
        for that keysym.
        """
        keysym = self.string_to_keysym.get(character, 0)
        if keysym == 0:
            keysym = self.string_to_keysym.get(KEYSYMS[character], 0)
        return self.display.keysym_to_keycode(keysym)

    def get_translation_dicts(self):
        """
        Returns dictionaries for the translation of keysyms to strings and from
        strings to keysyms.
        """
        keysym_to_string_dict = {}
        string_to_keysym_dict = {}
        #XK loads latin1 and miscellany on its own; load latin2-4 and greek
        Xlib.XK.load_keysym_group('latin2')
        Xlib.XK.load_keysym_group('latin3')
        Xlib.XK.load_keysym_group('latin4')
        Xlib.XK.load_keysym_group('greek')

        #Make a standard dict and the inverted dict
        for string, keysym in Xlib.XK.__dict__.items():
            if string.startswith('XK_'):
                string_to_keysym_dict[string[3:]] = keysym
                keysym_to_string_dict[keysym] = string[3:]
        return keysym_to_string_dict, string_to_keysym_dict

    def ascii_printable(self, keysym):
        """
        If the keysym corresponds to a non-printable ascii character this will
        return False. If it is printable, then True will be returned.

        ascii 11 (vertical tab) and ascii 12 are printable, chr(11) and chr(12)
        will return '\x0b' and '\x0c' respectively.
        """
        if 0 <= keysym < 9:
            return False
        elif 13 < keysym < 32:
            return False
        elif keysym > 126:
            return False
        else:
            return True
