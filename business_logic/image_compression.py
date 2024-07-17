from PIL import Image, ImageOps
import app.config
import glob

def resize_image(input_image_path, output_image_path, width_range, height_range, dpi=(300, 600)):

    for filename in glob.glob('input_image_path'): #assuming gif
        image_list = []
        # im=Image.open(filename)
        # image_list.append(im)
        output_image_path = output_image_path+'filename'
        # Open the original image
        original_image = Image.open(input_image_path)

        # Calculate the aspect ratio
        aspect_ratio = original_image.width / original_image.height

        # Determine target dimensions based on aspect ratio and range limits
        min_width, min_height = width_range[0], height_range[0]
        max_width, max_height = width_range[1], height_range[1]

        # Calculate target dimensions for portrait and landscape based on aspect ratio
        if aspect_ratio >= 1:  # Landscape or square
            target_width = min(max(original_image.width, min_width * dpi[0]), max_width * dpi[0])
            target_height = min(max(original_image.height, min_height * dpi[1]), max_height * dpi[1])
        else:  # Portrait
            target_height = min(max(original_image.height, min_height * dpi[0]), max_height * dpi[0])
            target_width = min(max(original_image.width, min_width * dpi[1]), max_width * dpi[1])

        # Resize the image
        resized_image = original_image.resize((int(target_width), int(target_height)))

        # Save the resized image as TIFF with LZW compression
        resized_image.save(output_image_path, compression="tiff_lzw", dpi=dpi)

if __name__ == "__main__":
    input_image = app.config['UPLOAD_FOLDER']+'*'  # Replace with your input image path
    output_image = app.config['DOWNLOAD_FOLDER']  # Replace with your output image path
    width_range = (2.63, 7.5)  # Min and max width in inches
    height_range = (0.25, 8.75)  # Min and max height in inches

    # DPI setting (300 x 600)
    dpi = (300, 600)

    # Resize the image
    resize_image(input_image, output_image, width_range, height_range, dpi)
