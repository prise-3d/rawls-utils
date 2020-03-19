# main imports
import argparse
import os, sys

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


def main():
    
    parser = argparse.ArgumentParser(description="Convert rawls folder into png images folder")

    parser.add_argument('--folder', type=str, help="folder with rawls images")
    parser.add_argument('--output', type=str, help="output expected folder")
    parser.add_argument('--flip', type=str, help="flip choice", choices=['h', 'v'])
    parser.add_argument('--ext', type=str, help="extension image choice", choices=['rawls', 'png'], default='png')


    args = parser.parse_args()

    p_folder  = args.folder
    p_output  = args.output
    p_flip    = args.flip
    p_ext     = '.' + args.ext

    # load all rawls images path of folder
    images = [img for img in sorted(os.listdir(p_folder)) if '.rawls' in img]
    number_of_images = len(images)

    if not os.path.exists(p_output):
        os.makedirs(p_output)

    for i, img in enumerate(images):

        img_path = os.path.join(p_folder, img)
        output_img_path = os.path.join(p_output, img.replace('.rawls', p_ext))
        # load and save image as png
        current_img = Rawls.load(img_path)

        if p_flip == 'h':
            current_img.h_flip()
        elif p_flip == 'v':
            current_img.v_flip()

        current_img.save(output_img_path)

        write_progress((i + 1) / number_of_images)

    print()

if __name__ == "__main__":
    main()