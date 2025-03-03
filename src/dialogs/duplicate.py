# duplicate.py
#
# Copyright 2020 brombinmirko <send@mirko.pm>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import time
from gi.repository import Gtk, Adw

from bottles.utils.threading import RunAsync  # pyright: reportMissingImports=false
from bottles.utils.gtk import GtkUtils
from bottles.backend.managers.backup import BackupManager


@Gtk.Template(resource_path='/com/usebottles/bottles/dialog-duplicate.ui')
class DuplicateDialog(Adw.Window):
    __gtype_name__ = 'DuplicateDialog'

    # region Widgets
    entry_name = Gtk.Template.Child()
    btn_cancel = Gtk.Template.Child()
    btn_duplicate = Gtk.Template.Child()
    stack_switcher = Gtk.Template.Child()
    progressbar = Gtk.Template.Child()
    ev_controller = Gtk.EventControllerKey.new()

    # endregion

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.set_transient_for(parent.window)

        # common variables and references
        self.parent = parent
        self.config = parent.config

        self.ev_controller.connect("key-released", self.__check_entry_name)
        self.entry_name.add_controller(self.ev_controller)

        # connect signals
        self.btn_cancel.connect("clicked", self.__close_window)
        self.btn_duplicate.connect("clicked", self.__duplicate_bottle)

    def __check_entry_name(self, *args):
        result = GtkUtils.validate_entry(self.entry_name)
        self.btn_duplicate.set_sensitive(result)

    def __close_window(self, widget=None):
        self.close()

    def __duplicate_bottle(self, widget):
        """
        This function take the new bottle name from the entry
        and create a new duplicate of the bottle. It also change the
        stack_switcher page when the process is finished.
        """
        self.stack_switcher.set_visible_child_name("page_duplicating")
        self.btn_duplicate.set_visible(False)
        self.btn_cancel.set_label("Close")

        RunAsync(self.pulse)
        name = self.entry_name.get_text()

        RunAsync(
            task_func=BackupManager.duplicate_bottle,
            callback=self.finish,
            config=self.config,
            name=name
        )

    def finish(self, result, error=None):
        # TODO: handle result.status == False
        self.parent.manager.update_bottles()
        self.stack_switcher.set_visible_child_name("page_duplicated")

    def pulse(self):
        # This function update the progress bar every half second.
        while True:
            time.sleep(.5)
            self.progressbar.pulse()
