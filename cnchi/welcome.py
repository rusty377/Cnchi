#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  welcome.py
#
#  Copyright © 2013,2014 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from gi.repository import Gtk, Gdk
import subprocess
import gettext
import os
import logging
import sys

import misc.misc as misc
import show_message as show

from gtkbasebox import GtkBaseBox

# Import functions
import config
try:
    import src.info as info
except ImportError:
    import info

class Welcome(GtkBaseBox):
    def __init__(self, params, prev_page=None, next_page="language"):
        super().__init__(self, params, "welcome", prev_page, next_page)

        data_dir = self.settings.get('data')
        welcome_dir = os.path.join(data_dir, "images", "welcome")

        self.labels = {'welcome': self.ui.get_object("welcome_label"), 'info': self.ui.get_object("info_welcome_label"),
                       'loading': self.ui.get_object("loading_label")}

        self.buttons = {'tryit': self.ui.get_object("tryit_button"), 'cli': self.ui.get_object("cli_button"),
                        'graph': self.ui.get_object("graph_button")}

        for key in self.buttons:
            btn = self.buttons[key]
            btn.set_name("welcome_btn")

        self.images = {'tryit': self.ui.get_object("tryit_image"), 'cli': self.ui.get_object("cli_image"),
                       'graph': self.ui.get_object("graph_image")}

        self.filenames = {'tryit': os.path.join(welcome_dir, "tryit-icon.png"),
                          'cli': os.path.join(welcome_dir, "cliinstaller-icon.png"),
                          'graph': os.path.join(welcome_dir, "installer-icon.png")}

        for key in self.images:
            self.images[key].set_from_file(self.filenames[key])

    def translate_ui(self):
        """ Translates all ui elements """
        if not self.disable_tryit:
            txt = _("You can try Antergos without making any changes to your system by selecting 'Try It'.") + "\n"
        else:
            txt = ""

        txt = txt + _("When you are ready to install Antergos simply choose which installer you prefer.")
        txt = '<span weight="bold">{0}</span>'.format(txt)
        self.labels['info'].set_markup(txt)

        txt = _("Try It")
        self.buttons['tryit'].set_label(txt)

        txt = _("CLI Installer")
        self.buttons['cli'].set_label(txt)

        txt = _("Graphical Installer")
        self.buttons['graph'].set_label(txt)

        txt = _("Welcome to Antergos!")
        self.header.set_subtitle(txt)

    def quit_cnchi(self):
        misc.remove_temp_files()
        self.settings.set('stop_all_threads', True)
        logging.shutdown()
        sys.exit(0)

    def on_tryit_button_clicked(self, widget, data=None):
        self.quit_cnchi()

    def on_cli_button_clicked(self, widget, data=None):
        try:
            subprocess.Popen(["antergos-wrap"])
            self.quit_cnchi()
        except Exception as err:
            msg = str(err)
            logging.error(msg)
            show.error(self.get_toplevel(), msg)

    def on_graph_button_clicked(self, widget, data=None):
        self.show_loading_message()
        # Tell timezone thread to start searching now
        self.settings.set('timezone_start', True)
        # Simulate a forward button click
        self.forward_button.clicked()

    def show_loading_message(self, show=True):
        if show:
            txt = _("Loading, please wait...")
        else:
            txt = ""
        self.labels['loading'].set_markup(txt)
        self.labels['loading'].queue_draw()
        misc.gtk_refresh()

    def store_values(self):
        self.forward_button.show()
        return True

    def prepare(self, direction):
        self.translate_ui()
        self.show_all()
        self.forward_button.hide()
        if self.disable_tryit:
            self.buttons['tryit'].set_sensitive(False)
        if direction == "backwards":
            self.show_loading_message(show=False)

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message): return message

if __name__ == '__main__':
    from test_screen import _,run
    run('Welcome')
