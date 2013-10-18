#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2013 Canonical Ltd.
# Author: Stéphane Graber <stgraber@ubuntu.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import glob
import os
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="image importer")
    parser.add_argument("path", metavar="DOWNLOAD-PATH")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        args.error("Invalid path: %s" % args.path)

    # Generate the list of download files
    downloads = []
    for entry in sorted(glob.glob("%s/*.tar.gz" % args.path)):
        file_name = os.path.basename(entry)
        gpg_name = None

        file_size = "%skB" % round(int(os.stat(entry).st_size) / 1024, 2)
        file_mdate = time.asctime(time.gmtime(os.path.getmtime(entry)))

        if os.path.exists("%s.asc" % args.path):
            gpg_column = "<a href=\"%s.asc\">%s.asc</a>" % (file_name,
                                                            file_name)
        else:
            gpg_column = "unavailable"

        file_column = "<a href=\"%s\">%s</a>" % (file_name, file_name)

        downloads.append((file_column, gpg_column, file_size, file_mdate))

    # Generate the html
    html = """    <table>
        <tr>
            <th>Filename</th>
            <th>GPG signature</th>
            <th>Size</th>
            <th>Last modified</th>
        </tr>
"""
    for download in downloads:
        html += """        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr>
""" % download
    html += "    </table>"

    with open(os.path.join(args.path, "index.html"), "w+") as fd_out:
        with open(os.path.join(args.path, "index.html.in"), "r") as fd_in:
            fd_out.write(fd_in.read().replace("@DOWNLOADS@", html))
