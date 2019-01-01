#!/usr/bin/env python
"""Script for clicking points in an image and saving their coordinates."""
import argparse
import cv2
import os
import numpy as np

# The clicked points
clicked_points = []


def redraw():
    for point in clicked_points:
        ipoint = (int(point[0]), int(point[1]))
        cv2.circle(img,
                   center=ipoint,
                   radius=3,
                   color=(0, 0, 255),
                   thickness=-1)
    cv2.imshow("clickable_image", img)


def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        clicked_points.append([float(x), float(y)])
        cv2.circle(img,
                   center=(x, y),
                   radius=3,
                   color=(0, 0, 255),
                   thickness=-1)
        cv2.imshow("clickable_image", img)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Click points in a picture"
                                     + " and save the coordinates.")
    parser.add_argument("input_img",
                        help="Input image file.",
                        type=str)
    parser.add_argument("-n",
                        action="store_true",
                        help="normalize coordinates, points range from 0 to "
                        + "1.",)
    parser.add_argument("-o", "--output_csv",
                        help="output file. Stored as csv. Defaults to the i"
                        + "nput_img filename with csv extension if not spec"
                        + "ified.",
                        default="",
                        type=str)
    args, unknown_args = parser.parse_known_args()

    # Read image
    original_img = cv2.imread(args.input_img)
    img = cv2.imread(args.input_img)

    # figure out output filename
    if len(args.output_csv) == 0:
        filename, file_ext = os.path.splitext(args.input_img)
        output_filename = filename + ".csv"
    else:
        if args.output_csv.endswith(".csv"):
            output_filename = args.output_csv
        else:
            output_filename = args.output_csv + ".csv"

    # Start up the window
    cv2.namedWindow("clickable_image", cv2.WINDOW_NORMAL)
    print("Clickable image: s to save and quit, q to quit without saving, z "
          + "to undo.")
    cv2.setMouseCallback("clickable_image", onMouse)
    cv2.imshow("clickable_image", img)
    while(True):
        key = cv2.waitKey(20) & 0xFF
        if key == ord("s"):
            # Save
            clicked_array = np.array(clicked_points)
            if args.n:
                clicked_array = clicked_array / clicked_array.max(axis=0)
            np.savetxt(output_filename, clicked_array,
                       delimiter=",", header="x, y")
            print("Saving then quitting.")
            break
        elif key == ord("q"):
            # quit without saving
            print("Quitting without saving.")
            break
        elif key == ord("z"):
            img = original_img.copy()
            if len(clicked_points) > 0:
                del clicked_points[-1]
                redraw()
