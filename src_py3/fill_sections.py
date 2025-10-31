import pandas as pd
import uuid

# Load the dataset
# df = pd.read_excel("Carson_Home_Accents_buyhere.xlsx")
df = pd.read_excel("Hanna's_Handiworks_Buyhere.xlsx")

# Function to assign sections based on product name and description
def assign_section(row):
    # If Sections (col V) is already filled, return it
    if pd.notna(row["Section"]) and row["Section"].strip():
        return row["Section"]
    
    # Get relevant columns for analysis
    product_name = str(row["Product Name"]).lower() if pd.notna(row["Product Name"]) else ""
    description = str(row["Detailed Product Description"]).lower() if pd.notna(row["Detailed Product Description"]) else ""
    
    # Combine text for keyword search
    combined_text = product_name + " " + description
    
    # Split product name by hyphen to extract product type
    product_type = ""
    if "-" in product_name:
        parts = product_name.split("-", 1)
        product_type = parts[0].strip()
    
    # Music Box
    if "music bx" in product_type or "music box" in product_type or "music bx" in combined_text:
        return "Music Box"
    
    # Message Bar
    if "msg bar" in product_type or "message bar" in product_type or "msg bar" in combined_text:
        return "Message Bar"
    
    # Tumbler
    if "tumbler" in product_type or "tumbler" in combined_text:
        return "Tumbler"
    
    # Stemless Wine
    if "stmls wine" in product_type or "stmls wine" in combined_text:
        return "Stemless Wine"
    
    # Mug
    if "mug" in product_type or "mug" in combined_text:
        return "Mug"
    
    # Rocks Glass
    if "rocks gl" in product_type or "rocks gl" in combined_text:
        return "Rocks Glass"
    
    # Trivet
    if "trivet" in product_type or "trivet" in combined_text:
        return "Trivet"
    
    # Coaster
    if "coaster" in product_type or "coaster" in combined_text:
        return "Coaster"
    
    # Can Cooler
    if "can cooler" in product_type or "can cooler" in combined_text:
        return "Can Cooler"
    
    # Tumbler
    if "tmblr" in product_type or "tmblr" in combined_text:
        return "Tumbler"
    
    # Beer can
    if "beer can" in product_type or "beer can" in combined_text:
        return "Beer Can"
    
    # Candle
    if "cdl" in product_type or "cdl" in combined_text:
        return "Candles"
    
    # Dish Cloth
    if "dish cloth" in product_type or "dish cloth" in combined_text:
        return "Dish Cloth"
    
    # Garden Stone
    if "garden stone" in product_type or "garden stone" in combined_text or "gdn/st" in combined_text:
        return "Garden Stone"
    
    # Garden Stake
    if "garden stake" in product_type or "garden stake" in combined_text or "cylinder stake" in combined_text or "gdn stk" in combined_text or "pole/stk" in combined_text:
        return "Garden Stake"
    
    # Step Stone
    if "step/stone" in product_type or "step/stone" in combined_text:
        return "Step Stone"
    
    # Paver
    if "paver" in product_type or "paver" in combined_text:
        return "Paver"
    
    # Birdhouse
    if "birdhouse" in product_type or "birdhouse" in combined_text:
        return "Birdhouses"
    
    # Wind Chime
    if "wind chime" in product_type or "wind chime" in combined_text or "chime" in combined_text:
        return "Wind Chime"
    
    # Frame
    if "frame" in product_type or "frame" in combined_text:
        return "Frame"
    
    # Wall Art
    if "wall art" in product_type or "wall art" in combined_text:
        return "Wall Art"
    
    # Wall Decor
    if "wall decor" in product_type or "wall decor" in combined_text or "wall dec" in combined_text:
        return "Wall Decor"
    
    # Wall Sign
    if "wall sign" in product_type or "wall sign" in combined_text:
        return "Wall Sign"
    
    # Hanging Sign
    if "hanging sign" in product_type or "hanging sign" in combined_text:
        return "Hanging Sign"
    
    # Photo bar
    if "photo bar" in product_type or "photo bar" in combined_text:
        return "Photo Bar"
    
    # Sitters
    if "sitter" in product_type or "sitter" in combined_text:
        return "Sitters"
    
    # Plaque
    if "plaque" in product_type or "plaque" in combined_text or "plq" in combined_text:
        return "Plaques"
    
    # Decorative Lantern
    if "lantern" in product_type or "lantern" in combined_text:
        return "Decorative Lantern"
    
    # Ornament
    if "ornament" in product_type or "orn" in product_type or "ornament" in combined_text:
        return "Ornaments"
    
    # Throw
    if "throw" in product_type or "throw" in combined_text:
        return "Throws"
    
    # Quilt
    if "quilt" in product_type or "quilt" in combined_text:
        return "Quilt"
    
    # Hanger
    if "hanger" in product_type or "hanger" in combined_text:
        return "Hanger"
    
    # Door Mat
    if "door mat" in product_type or "door mat" in combined_text or " mat" in combined_text:
        return "Door Mat"
    
    # Mailbox Cover
    if "mailbox cover" in product_type or "mailbox cover" in combined_text:
        return "Mailbox Cover"
    
    # Accent Rug
    if "accent rug" in product_type or "accent rug" in combined_text or "rug" in combined_text:
        return "Accent Rug"
    
    # Floral
    if "floral" in product_type or "floral" in combined_text:
        return "Floral"
    
    # Plush
    if "plush" in product_type or "plush" in combined_text:
        return "Plush"
    
    # Wall Plaque
    if "wall plq" in product_type or "wall plq" in combined_text:
        return "Wall Plaque"
    
    # Shot glass
    if "shot glass" in product_type or "shot glass" in combined_text or "shot gl" in combined_text:
        return "Shot Glass"
    
    # Sonnet
    if " son" in product_type or " son" in combined_text:
        return "Sonnet"
    
    # Chimes
    if " ch" in product_type or " ch" in combined_text or " chm" in combined_text:
        return "Chimes"
    
    # Serving Board
    if "serving board" in product_type or "serving board" in combined_text:
        return "Serving Board"
    
    # Decanter
    if "decanter" in product_type or "decanter" in combined_text:
        return "Decanter"
    
    # Magnet
    if "magnet" in product_type or "magnet" in combined_text:
        return "Magnet"
    
    # Memory Box
    if "memory box" in product_type or "memory box" in combined_text:
        return "Memory and Keepsake Boxes"
    
    # Wall Cross
    if "wall cross" in product_type or "wall cross" in combined_text:
        return "Wall Cross"
    
    # Bottle opener
    if "btl opnr" in product_type or "btl opnr" in combined_text:
        return "Bottle Opener"
    
    
    # Fallback to Decor for unclassified decorative items
    return "Decor"

# Apply the section assignment to Column V
df["Sections"] = df.apply(assign_section, axis=1)

# Save the updated dataset
output_file = f"Carson_Home_Accents_buyhere_updated_sections_{uuid.uuid4().hex}.xlsx"#
df.to_excel(output_file, index=False)

print(f"Updated dataset saved as {output_file}")