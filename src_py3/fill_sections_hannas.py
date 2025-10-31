import pandas as pd
import uuid

# Load the dataset
df = pd.read_excel("Hanna's_Handiworks_Buyhere.xlsx")

# Function to assign sections based on product name and description
def assign_section(row):
    # If Section (col V) is already filled, return it
    if pd.notna(row["Section"]) and row["Section"].strip():
        return row["Section"]
    
    # Get relevant columns for analysis
    product_name = str(row["Product Name"]).lower() if pd.notna(row["Product Name"]) else ""
    description = str(row["Detailed Product Description"]).lower() if pd.notna(row["Detailed Product Description"]) else ""
    
    # Combine text for keyword search
    combined_text = product_name + " " + description
    
    # Split product name by hyphen to extract product type
    product_type = product_name
    # if "-" in product_name:
    #     parts = product_name.split("-", 1)
    #     product_type = parts[0].strip()
    
    # Wall Decor
    if "wall decor" in product_type or "wall decor" in combined_text or "wall art" in combined_text:
        return "Wall Decor"
    
    # Hangers
    if "hanger" in product_type or "hanger" in combined_text or "hook" in combined_text:
        return "Hangers"
    
    # Tabletop
    if "tabletop" in product_type or "tabletop" in combined_text or "tt" in product_type or "shelf sitter" in combined_text:
        return "Tabletop"
    
    # Frames & Table Decor
    if "frame" in product_type or "frame" in combined_text or "photo" in combined_text or "frames & table decor" in combined_text:
        return "Frames & Table Decor"
    
    # Ornaments
    if "ornament" in product_type or " orn " in product_type or "ornament" in combined_text:
        return "Ornaments"
    
    # Snowmen & Santas
    if "snowman" in product_type or "santa" in product_type or "snowman" in combined_text or "santa" in combined_text:
        return "Snowmen & Santas"
    
    # Plush
    if "dangle leg" in product_type or "stretch leg" in product_type or "stander" in product_type or "sitter" in product_type or "bobble" in product_type or "plush" in combined_text or "fabric" in description:
        return "Plush"
    
    # Gnomes, Moose & Seasonal
    if "gnome" in product_type or "moose" in product_type or "elf" in product_type or "gnome" in combined_text or "moose" in combined_text or "elf" in combined_text:
        return "Gnomes, Moose & Seasonal"
    
    # Containers & Bins
    if "bucket" in product_type or "tub" in product_type or "basket" in product_type or "bucket" in combined_text or "tub" in combined_text or "basket" in combined_text:
        return "Containers & Bins"
    
    # Kitchen & Entertaining
    if "salt and pepper" in product_type or "serving tray" in product_type or "plate" in product_type or "salt and pepper" in combined_text or "serving tray" in combined_text or "plate" in combined_text:
        return "Kitchen & Entertaining"
    
    # Metal Decor
    if "metal decor" in product_type or "metal decor" in combined_text:
        return "Metal Decor"
    
    # Trees & Skirts
    if "tree" in product_type or "skirt" in product_type or "tree" in combined_text or "skirt" in combined_text:
        return "Trees & Skirts"
    
    # Signs
    if "sign" in product_type or "sign" in combined_text or "plaque" in combined_text:
        return "Signs"
    
    # Birdhouses
    if "birdhouse" in product_type or "birdhouse" in combined_text:
        return "Birdhouses"
    
    # Wind Chime
    if "wind chime" in product_type or "wind chime" in combined_text or "windchime" in combined_text:
        return "Wind Chime"
    
    # Fallback to Decor for unclassified decorative items
    return "Decor"

# Apply the section assignment to Column V
df["Section"] = df.apply(assign_section, axis=1)

# Save the updated dataset
output_file = f"Hanna's_Handiworks_Buyhere_updated_sections_{uuid.uuid4().hex}.xlsx"
df.to_excel(output_file, index=False)

print(f"Updated dataset saved as {output_file}")