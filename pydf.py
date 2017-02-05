#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from reportlab.pdfgen import canvas
from PIL import Image
 
import argparse, shlex

POINTS_PER_INCH = 72

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Assembles images in a PDF file, without altering the images.')
    parser.add_argument("manifest", type=argparse.FileType("r"),
                         help="A manifest file, listing the images added to the PDF, in pages order)."
                              "Optionaly, it can specify each image resolution (in dpi), as a single value, or as a pair."
                              "The format is \"image_file [dpi | x_dpi y_dpi]\", one per line.")
    parser.add_argument("output", type=argparse.FileType("wb"), help="The generated PDF file.")
    args = parser.parse_args()

    c = canvas.Canvas(args.output)

    for line in args.manifest:
        image_info = shlex.split(line) 

        if len(image_info)==0 or image_info[0].startswith("#"):
            continue

        # Read the image
        image = Image.open(image_info[0])

        # Decide on the DPI to use
        dpi = None
        if len(image_info) > 1:
            dpi = (int(image_info[1]), int(image_info[2 if len(image_info)>2 else 1]))
        if dpi is None:
            try:
                dpi = image.info["dpi"]
            except KeyError:
                raise Exception("The DPI info cannot be found for image \"{}\"".format(image_info[0]))

        # Compute the page size based on the DPI
        size_in_points = [pixel_size/dpi * POINTS_PER_INCH for pixel_size, dpi in zip(image.size, dpi)]
        print("Size: {}, Dpi: {}, Point size: {}".format(image.size, dpi, size_in_points))
        c.setPageSize((size_in_points))

        ## From teh doc, drawImage should be able to accept a PIL image for the first argument, but that fails.
        #c.drawImage(image, 0, 0, width=size_in_points[0], height=size_in_points[1])
        c.drawImage(image_info[0], 0, 0, width=size_in_points[0], height=size_in_points[1])
        c.showPage()

    c.save()
