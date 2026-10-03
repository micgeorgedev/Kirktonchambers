from PIL import Image
import glob
import os
import colorsys

def recolor_pixel(r, g, b):
    # Convert to HSV
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    
    # Check if pixel is "reddish" (Hue near 0 or 1, high enough saturation)
    # Red hue is around 0.95 to 1.0, or 0.0 to 0.05.
    if (h > 0.85 or h < 0.1) and s > 0.2:
        # Target gold: #c5a971 -> RGB(197, 169, 113) -> HSV(~39/360, 0.42, 0.77)
        # We shift hue to ~40/360 = 0.111
        # We can also scale saturation down slightly if it's too bright red
        target_h = 40.0 / 360.0
        
        # New HSV
        new_r, new_g, new_b = colorsys.hsv_to_rgb(target_h, s * 0.7, v)
        return int(new_r * 255), int(new_g * 255), int(new_b * 255)
    
    # Also check if it's the specific navy #1d2544 -> #0f1b33
    # #1d2544 -> RGB(29, 37, 68), #0f1b33 -> RGB(15, 27, 51)
    if (0.5 < h < 0.7) and v < 0.4:
        # Shift slightly darker/deeper navy
        target_h_navy = 220.0 / 360.0 # ~0.61
        new_r, new_g, new_b = colorsys.hsv_to_rgb(target_h_navy, s, v * 0.8)
        return int(new_r * 255), int(new_g * 255), int(new_b * 255)

    return r, g, b

files = glob.glob('/root/Kirktonchambers/wp-content/themes/kirkton-chambers/assets/img/**/*.png', recursive=True) + \
        glob.glob('/root/Kirktonchambers/wp-content/themes/kirkton-chambers/assets/img/**/*.jpg', recursive=True) + \
        glob.glob('/root/Kirktonchambers/wp-content/uploads/**/*.png', recursive=True) + \
        glob.glob('/root/Kirktonchambers/wp-content/uploads/**/*.jpg', recursive=True)

processed = 0
for filepath in files:
    try:
        img = Image.open(filepath)
        img = img.convert("RGBA")
        data = img.getdata()
        
        new_data = []
        changed = False
        
        for item in data:
            if item[3] == 0: # Transparent
                new_data.append(item)
                continue
                
            new_r, new_g, new_b = recolor_pixel(item[0], item[1], item[2])
            if (new_r, new_g, new_b) != (item[0], item[1], item[2]):
                changed = True
                
            new_data.append((new_r, new_g, new_b, item[3]))
            
        if changed:
            img.putdata(new_data)
            # Save original format
            if filepath.lower().endswith('.jpg') or filepath.lower().endswith('.jpeg'):
                img.convert('RGB').save(filepath, quality=90)
            else:
                img.save(filepath)
            processed += 1
            print(f"Recolored {filepath}")
            
    except Exception as e:
        print(f"Failed {filepath}: {e}")

print(f"Done. Processed {processed} images.")
