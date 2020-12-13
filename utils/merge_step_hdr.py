# main imports
import argparse
import os, sys
import numpy as np
import cv2
import math

# Images imports
from rawls.rawls import Rawls


def write_progress(progress):
    '''
    Display progress information as progress bar
    '''
    barWidth = 180

    output_str = "["
    pos = barWidth * progress
    for i in range(barWidth):
        if i < pos:
           output_str = output_str + "="
        elif i == pos:
           output_str = output_str + ">"
        else:
            output_str = output_str + " "

    output_str = output_str + "] " + str(int(progress * 100.0)) + " %\r"
    print(output_str)
    sys.stdout.write("\033[F")


def __clamp(n, smallest, largest):
    """Clamp number using two numbers
    
    Arguments:
        n: {float} -- the number to clamp
        smallest: {float} -- the smallest number interval
        largest: {float} -- the larget number interval
    
    Returns:
        {float} -- the clamped value

    Example:

    >>> from rawls.rawls import Rawls
    >>> path = 'images/example_1.rawls'
    >>> rawls_img = Rawls.load(path)
    >>> rawls_img._Rawls__clamp(300, 0, 255)
    255
    >>> rawls_img._Rawls__clamp(200, 0, 255)
    200
    """
    return max(smallest, min(n, largest))

def __gamma_correct(value):
    """Correct gamma of luminance value
    
    Arguments:
        value: {float} -- luminance value to correct
    
    Returns:
        {float} -- correct value with specific gamma

    Example:

    >>> from rawls.rawls import Rawls
    >>> path = 'images/example_1.rawls'
    >>> rawls_img = Rawls.load(path)
    >>> rawls_img._Rawls__gamma_correct(0.80)
    0.9063317533440594
    >>> rawls_img._Rawls__gamma_correct(0.55)
    0.7673756580558262
    """
    if value <= 0.0031308:
        return 12.92 * value
    else:
        return 1.055 * math.pow(value, float(1. / 2.4)) - 0.055


def __gamma_convert(value):
    """Correct gamma value and clamp it
    
    Arguments:
        value: {float} -- luminance value to correct and clamp
    
    Returns:
        {float} -- final chanel value
    """

    # TODO : check this part
    return __clamp(255. * __gamma_correct(value) + 0., 0., 255.)
    # remove clamp conversion
    #return __gamma_correct(value)


def convert_np_gamma(instance):

    data_arr = np.array(instance.data, copy=True)
    height, width, chanels = data_arr.shape

    for y in range(height):
        for x in range(width):
            for c in range(chanels):
                data_arr[y][x][c] = __gamma_convert(data_arr[y][x][c])

    return data_arr


def main():
    
    parser = argparse.ArgumentParser(description="Convert rawls folder into png images folder")

    parser.add_argument('--folder', type=str, help="folder with rawls images", required=True)
    parser.add_argument('--output', type=str, help="output expected folder", required=True)
    parser.add_argument('--step', type=int, help="step number of samples", required=True)
    parser.add_argument('--mult', type=int, help="multiplicator impact indices", default=0)
    #parser.add_argument('--gamma', type=int, help="extension image choice", choices=[0, 1], default=1)

    args = parser.parse_args()

    p_folder  = args.folder
    p_output  = args.output
    p_step    = args.step
    p_mult    = args.mult
    #p_gamma   = bool(args.gamma)

    # load all rawls images path of folder
    images = [img for img in sorted(os.listdir(p_folder)) if '.rawls' in img]
    number_of_images = len(images)

    if not os.path.exists(p_output):
        os.makedirs(p_output)

    merged_img = None

    for i, img in enumerate(images):

        img_path = os.path.join(p_folder, img)

        if merged_img:
            current_img = Rawls.load(img_path)
            merged_img = Rawls.fusion(current_img, merged_img)
        else:
            merged_img = Rawls.load(img_path)
       
        if merged_img.details.samples % p_step == 0:
            
            # build output images index
            index_str = str(merged_img.details.samples)
            print(f"Number of samples is now of {index_str}")

            while len(index_str) < 5:
                index_str = "0" + index_str

            # build output image path name and path
            _, basename =  os.path.split(p_output)
            output_image_name = basename + '_' + index_str + '.hdr'
            output_img_path = os.path.join(p_output, output_image_name)
            print(output_img_path)

            # load and save image as png
            # print(p_gamma)
            # merged_img.save(output_img_path, p_gamma)
            gamma_image = convert_np_gamma(merged_img)
            cv2.imwrite(output_img_path, gamma_image)

        # update progress information
        write_progress((i + 1) / number_of_images)

    print()

if __name__ == "__main__":
    main()