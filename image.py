from PIL import Image, ImageEnhance
import os

mypath = r"C:\Users\Sayed\OneDrive\Desktop\Resize_pic"

def resize_images(*images): 
    
    # Desired size
    new_size = (1400, 800)

    # Folder to save resized images
    output_folder = r"C:\Users\Sayed\OneDrive\Desktop\Resize_pic\Resized"

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through each image path
    for image_path in images:
        # Open the image
        img = Image.open(image_path)
        
        # Print original image dimensions
        print(' ')
        print('*'*50)
        print(f"Original size of {image_path}: {img.width}x{img.height}\n")
        
        # Convert to RGB mode if necessary
        if img.mode == 'P':
            img = img.convert('RGB')
        
        # Resize the image with a resampling filter (try different filters)
        img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Enhance the image (optional)
        sharpness_enhancer = ImageEnhance.Sharpness(img_resized)
        img_resized = sharpness_enhancer.enhance(1.5)

        contrast_enhancer = ImageEnhance.Contrast(img_resized)
        img_resized = contrast_enhancer.enhance(1.2)

        brightness_enhancer = ImageEnhance.Brightness(img_resized)
        img_resized = brightness_enhancer.enhance(1.1)


        # Show the resized image (optional)
        # img_resized.show()
        
        # Get the filename from the path
        filename = os.path.basename(image_path)
        
        # Save the resized image to the output folder
        img_resized.save(os.path.join(output_folder, filename))
        
        # Print confirmation
        print(f"Resized image saved as {os.path.join(output_folder, filename)}\n")

    print("All images have been resized.\n")
    print("*" * 50)

# To Degine work, call it:    
resize_images(os.path.join(mypath,"CIB.png"),
              os.path.join(mypath, "hand.jpg")
              )