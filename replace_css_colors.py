import re

css_path = '/root/Kirktonchambers/wp-content/themes/kirkton-chambers/assets/css/global675f.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace dark navy
css = re.sub(r'#1d2544', '#0f1b33', css, flags=re.IGNORECASE)

# Replace red with gold.
# For text color, we want a darker gold #8a6d2f for contrast. For backgrounds/borders, #c5a971.
# We can do this by finding "color: #d70c3d" and replacing with #8a6d2f
css = re.sub(r'color\s*:\s*#d70c3d', 'color: #8a6d2f', css, flags=re.IGNORECASE)
# The rest of #d70c3d (backgrounds, borders) become #c5a971
css = re.sub(r'#d70c3d', '#c5a971', css, flags=re.IGNORECASE)

# Also fix the hero overrides in index.html, though we might have already used #c5a971 there.
html_path = '/root/Kirktonchambers/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'#1d2544', '#0f1b33', html, flags=re.IGNORECASE)
html = re.sub(r'#d70c3d', '#c5a971', html, flags=re.IGNORECASE)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("CSS colors updated.")
