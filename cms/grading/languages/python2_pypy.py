#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2016-2018 Stefano Maggiolo <s.maggiolo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Python programming language, version 2, definition."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.builtins.disabled import *  # noqa
from future.builtins import *  # noqa

import os

from cms.grading import CompiledLanguage


__all__ = ["Python2PyPy"]


class Python2PyPy(CompiledLanguage):
    """This defines the Python programming language, version 2 (more
    precisely, the subversion of Python 2 made available by the PyPy
    interpreter on the system, usually 2.7).

    """

    MAIN_FILENAME = "__main__.pyc"

    @property
    def name(self):
        """See Language.name."""
        return "Python 2 / PyPy"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".py"]

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        zip_filename = "%s.zip" % executable_filename

        commands = []
        files_to_package = []
        for idx, source_filename in enumerate(source_filenames):
            commands.append(["/usr/bin/pypy", "-m", "py_compile", source_filename])

            basename = os.path.splitext(os.path.basename(source_filename))[0]
            pyc_file_pattern = os.path.join("__pycache__", "%s.pypy*.pyc" % basename)
            # The file with the entry point must be in first position.
            if idx == 0:
                commands.append(["/usr/bin/find", "__pycache__/",
                    "-type", "f",
                    "-name", "%s.pypy*.pyc" % basename,
                    "-exec", "/bin/mv", "{}", self.MAIN_FILENAME, ";"])
                files_to_package.append(self.MAIN_FILENAME)
            else:
                files_to_package.append(pyc_filename)

        # zip does not support writing to a file without extension.
        commands.append(["/usr/bin/zip", "-r", zip_filename]
                        + files_to_package)
        commands.append(["/bin/mv", zip_filename, executable_filename])

        return commands

    def get_evaluation_commands(
            self, executable_filename, main=None, args=None):
        """See Language.get_evaluation_commands."""
        args = args if args is not None else []
        return [["/usr/bin/pypy", executable_filename] + args]