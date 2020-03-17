# main imports
import argparse
import os, sys

# Images imports
from rawls.classes.rawls import Rawls


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
    parser.add_argument('--step', type=int, help="step number of samples")
    parser.add_argument('--ext', type=str, help="extension image choice", choices=['rawls', 'png'], default='png')

    args = parser.parse_args()

    p_folder  = args.folder
    p_output  = args.output
    p_step    = args.step
    p_ext     = '.' + args.ext

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

            while len(index_str) < 5:
                index_str = "0" + index_str

            # build output image path name and path
            output_image_name = p_output + '_' + index_str + p_ext
            output_img_path = os.path.join(p_output, output_image_name)

            # load and save image as png
            merged_img.save(output_img_path)

        # update progress information
        write_progress((i + 1) / number_of_images)

    print()

if __name__ == "__main__":
    main()