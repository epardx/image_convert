#!/usr/bin/env python
import argparse
from PIL import Image

def image_convert(file_name):
    img = Image.open(file_name).convert('L')  # convert image to 8-bit grayscale
    # img.show() # demonstrate image input
    adj_img = img.resize((40, 40)) # adjust image to appropriate size
    # adj_img.show() # demonstrate new image
    WIDTH, HEIGHT = adj_img.size
    
    data = list(adj_img.getdata())  # convert image data to a list of integers
    # convert that to 2D list (list of lists of integers)
    data = [data[offset:offset + WIDTH] for offset in range(0, WIDTH * HEIGHT, WIDTH)]

    # At this point the image's pixels are all in memory and can be accessed
    # individually using data[row][col].

    # For example:
    file = open("ui_out.txt", "w")
    for row in data:
        # print(' '.join('{:3}'.format(value) for value in row)) # Print to console
        file.write(' '.join('{:3}'.format(value) for value in row))
        file.write('\n')
    file.close()

# For running in cmd prompt
##    if args.output_file:
##        with open(args.output_file, 'w') as output_file:
##            for row in data:
##                output_file.write(' '.join('{:3}'.format(value) for value in row))
##                output_file.write('\n')


if __name__ == '__main__':
    # For running in cmd
    parser = argparse.ArgumentParser(description='cmd processor for image convert')
    parser.add_argument("cmd", help="Commands can be: convert")
    parser.add_argument('--i', dest='input_file')
    parser.add_argument('--o', dest='output_file')
    args = parser.parse_args()
    command = args.cmd

    if command == 'convert':
        if args.input_file is None:
            print("Usage: python image_convert.py convert --i image-file-name")
        else:
            file_path = args.input_file
        image_convert(file_path)

