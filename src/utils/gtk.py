# gtk.py
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


class GtkUtils:

    @staticmethod
    def validate_entry(entry) -> bool:
        regex = re.compile("[@!#$%^&*()<>?/|}{~:.;,'\"]")
        text = entry.get_text()

        if (regex.search(text) is None) and text != "" and not text.isspace():
            entry.remove_css_class("error")
            return True

        entry.add_css_class("error")
        return False
