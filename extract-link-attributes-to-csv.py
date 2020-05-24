#!/usr/bin/env python3
# -------------------------------------------------------------------------------
# Name:             Extract PTV Vissim Link Attributes
# Purpose:          Extract all link type, link width, lane numbers
#                   and coordinates from PTV Vissim
#
# Author:           jh205
# Contributor:      jaredbest
#
# Creation Date:    2017-04-01
# Modified On:      2020-05-06
# Copyright:        (c) jh205 2017
# Licence:          <ICL>
# -------------------------------------------------------------------------------

import xml.etree.ElementTree as ET
import csv
import tkinter as tk
from tkinter import filedialog


def main():

    # Open file dialog to select PTV Vissim network file (INPX):
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()

    tree = ET.parse(filename)
    root = tree.getroot()

    link_dict = {}

    for link_element in root.findall('./links/link'):
        link_number = int(link_element.get('no'))  # Get link number
        link_dict[link_number] = []

        for lane_element in link_element.findall('./lanes'):
            lane_count = len(lane_element.findall('lane'))

        # Get link width and lane number
        for lane_width in link_element.findall('./lanes/lane'):
            # Check whether link is connector or link
            if lane_width.get('width') is None:
                linkType = 'connector'
            if lane_width.get('width') is not None:
                linkType = 'link'

        # Currently lane width is coded as standard width,
        # if different in model, specify
        link_width = 3.5 * lane_count
        link_dict[link_number].append(linkType)
        link_dict[link_number].append(link_width)
        link_dict[link_number].append(lane_count)

        # Get link coordinates
        for coords in link_element.findall('./geometry/linkPolyPts/linkPolyPoint'):
            coords_startX = float(coords.get('x'))
            coords_startY = float(coords.get('y'))
            coords_startZ = float(coords.get('zOffset'))
            link_dict[link_number].append(
                (coords_startX, coords_startY, coords_startZ))

    with open('out.csv', 'w') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Link No.', 'Link or Connector', 'Link Width (m)',
                    'Lane No.', 'Start x', 'Start y', 'Start zOffset',
                    'End x', 'End y', 'End zOffset'])
        for key in sorted(link_dict):
            coords_array = link_dict[key]
            coords_array_length = len(coords_array)
            start_x = coords_array[3][0]
            start_y = coords_array[3][1]
            start_z = coords_array[3][2]
            end_x = coords_array[coords_array_length-1][0]
            end_y = coords_array[coords_array_length-1][1]
            end_z = coords_array[coords_array_length-1][2]
            link_type = coords_array[0]
            link_width = coords_array[1]
            lane_no = coords_array[2]
            w.writerow([key, link_type, link_width, lane_no,
                        start_x, start_y, start_z, end_x, end_y, end_z])


if __name__ == '__main__':
    main()
