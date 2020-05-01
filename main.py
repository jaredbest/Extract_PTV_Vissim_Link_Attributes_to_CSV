#!/usr/bin/env python3

# -------------------------------------------------------------------------------
# Name:             Extract PTV Vissim Network Info
# Purpose:          Extract all link type, link width, lane numbers
#                   and coordinates from PTV Vissim
#
# Author:           jh205
# Contributor:      jaredbest
#
# Creation Date:    2017-04-01
# Copyright:        (c) jh205 2017
# Licence:          <ICL>
# -------------------------------------------------------------------------------

import xml.etree.ElementTree as ET
import csv

# Specify PTV Vissim network file (INPX):
filename = "network.inpx"

tree = ET.parse(filename)
root = tree.getroot()

link_dict = {}

for link_element in root.findall('./links/link'):
    link_number = int(link_element.get('no'))  # Get link number
    link_dict[link_number] = []

    for laneElement in link_element.findall('./lanes'):
        lane_number = len(laneElement.findall('lane'))

    # Get link width and lane number
    for lane_width in link_element.findall('./lanes/lane'):
        # Check whether link is connector or link
        if lane_width.get('width') is None:
            linkType = 'connector'
        if lane_width.get('width') is not None:
            linkType = 'link'

    # Currently lane width is coded as standard width,
    # if different in model, specify
    link_width = 3.5 * lane_number
    link_dict[link_number].append(linkType)
    link_dict[link_number].append(link_width)
    link_dict[link_number].append(lane_number)

    # Get link coordinates
    for coords in link_element.findall('./geometry/linkPolyPts/linkPolyPoint'):
        coords_startX = float(coords.get('x'))
        coords_StartY = float(coords.get('y'))
        link_dict[link_number].append((coords_startX, coords_StartY))

with open('out.csv', 'w') as f:
    w = csv.writer(f, delimiter=',')
    w.writerow(['link_id', 'link_type', 'link_width(m)',
                'lane_no', 'start_x', 'start_y', 'end_x', 'end_y'])
    for key in sorted(link_dict):
        coords_array = link_dict[key]
        coords_array_length = len(coords_array)
        start_x = coords_array[3][0]
        start_y = coords_array[3][1]
        end_x = coords_array[coords_array_length-1][0]
        end_y = coords_array[coords_array_length-1][1]
        link_type = coords_array[0]
        link_width = coords_array[1]
        lane_no = coords_array[2]
        w.writerow([key, link_type, link_width, lane_no,
                    start_x, start_y, end_x, end_y])
