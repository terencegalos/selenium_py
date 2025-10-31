import pandas as pd
import uuid

# Load the dataset
df = pd.read_excel("Carson_Home_Accents_buyhere.xlsx")

# Function to assign categories based on product name and description
def assign_category(row):
    # If Store Categories (col T) is already filled, return it
    if pd.notna(row["Store Categories"]) and row["Store Categories"].strip():
        return row["Store Categories"]
    
    # Get relevant columns for analysis
    product_name = str(row["Product Name"]).lower() if pd.notna(row["Product Name"]) else ""
    description = str(row["Detailed Product Description"]).lower() if pd.notna(row["Detailed Product Description"]) else ""
    
    # Combine text for keyword search
    combined_text = product_name + " " + description
    
    # Split product name by hyphen to extract sentiment/theme
    sentiment = ""
    if "-" in product_name:
        parts = product_name.split("-", 1)
        if len(parts) > 1:
            sentiment = parts[1].strip()
    
    # Bereavement-related keywords
    if any(keyword in combined_text for keyword in [
        "memorial", "bereavement", "angel", "in loving memory", "loving memory", "cardinal", "memory lives",
        "beautiful soul", "heaven", "forever missed", "rainbow bridge", "memory", "time passes", "your memory",
        "memories", "in remembrance"
    ]):
        return "(All) Carson Home Accents|Bereavement"
    
    # Christian & Inspirational keywords
    if any(keyword in combined_text for keyword in [
        "amazing grace", "cross", "serenity prayer", "blessed", "god's plan", "pray more",
        "faith", "in his keeping"
    ]):
        return "(All) Carson Home Accents|Christian & Inspirational"
    
    # Beach & Seashore keywords
    if any(keyword in sentiment for keyword in [
        "beach more", "salt water", "sunshine", "flip flops", "sun sand"
    ]) or any(keyword in combined_text for keyword in [
        "beach", "seashore", "coastal", "mermaid", "starfish"
    ]):
        return "(All) Carson Home Accents|Beach & Seashore"
    
    # Lodge, Cabin & Lake keywords
    if any(keyword in sentiment for keyword in [
        "campfire", "adventure", "lake life", "happy camp"
    ]) or any(keyword in combined_text for keyword in [
        "lodge", "cabin", "lake", "camping", "mountain", "wild", "bear"
    ]):
        return "(All) Carson Home Accents|Lodge, Cabin & Lake"
    
    # Farmhouse keywords
    if any(keyword in sentiment for keyword in [
        "farm sweet farm", "howdy y’all", "pasture", "rural"
    ]) or any(keyword in combined_text for keyword in [
        "farm", "farmhouse", "rooster", "bacon"
    ]):
        return "(All) Carson Home Accents|Farmhouse"
    
    # Kitchen-related items
    if any(keyword in combined_text for keyword in [
        "tumbler", "mug", "coaster", "dish cloth", "vase", "dip chiller", "bottle", "can cooler",
        "stmls wine", "serving board", "btl opnr", "shot gl", "tmblr", "rocks gl", "trivet"
    ]):
        return "(All) Carson Home Accents|Kitchen & Entertaining"
    
    # Garden-related items
    if any(keyword in combined_text for keyword in [
        "garden stone", "garden stake", "birdhouse", "trellis", "cylinder stake", "garden trellis"
    ]):
        return "(All) Carson Home Accents|Garden & Outdoor"
    
    # Pet-related items
    if any(keyword in combined_text for keyword in [
        "dog", "cat", "pet", "paw print"
    ]):
        return "(All) Carson Home Accents|Pets & Home"
    
    # Christmas-related items
    if any(keyword in combined_text for keyword in [
        "xmas", "christmas", "ornament", "merry", "merry everything", "snowflakes", "joy", "jingle", "holiday cheer",
        "sleigh", "jolly", "ho ho ho", "believe", "peace on earth", "merry & bright", "deck the halls",
        "santa", "noel", "jingle all the way", "holiday", "christmas tree", "reindeer",
        "christmas cheer", "holiday season", "festive", "winter wonderland", "sleigh bells",
        "freeze", "snowman", "holiday spirit", "jingle bells", "sleigh ride", "mistletoe",
        "holiday magic", "santa's workshop", "christmas eve", "holiday lights",
        "wonderland", "holiday greetings", "santa claus", "christmas carol",
        "gingebread", "holiday traditions", "christmas spirit", "holiday joy",
        "holly", "holy night", "snowy", "winter", "frosty", "jolly old st. nick",
        "snwmn"
    ]):
        return "(All) Carson Home Accents|Christmas"
    
    # Spring & Easter-related items
    if any(keyword in combined_text for keyword in [
        "easter", "spring", "bunny", "egg", "blossom", "butterfly", "flower", "bloom",
        "springtime", "hoppy", "blooming", "egg hunt", "spring fling", "easter egg",
        "he is risen", "spring has sprung", "spring flowers", "easter basket",
        "bunnies", "spring decor", "easter decorations", "spring vibes",
    ]):
        return "(All) Carson Home Accents|Spring & Easter"
    
    # Americana & Patriotic items
    if any(keyword in combined_text for keyword in [
        "patriotic", "independence", "freedom", "stars & stripes", "red white blue", "flag"
    ]) or any(keyword in sentiment for keyword in [
        "land of the free", "home of the brave"
    ]):
        return "(All) Carson Home Accents|Americana"
    
    # Humorous or light-hearted items
    if any(keyword in combined_text for keyword in [
        "coffee & wine", "dad bod", "tipsy", "bad influence", "starvation", "therapy", "drink happy",
        "day drinking", "zest", "peachy clean"
    ]):
        return "(All) Carson Home Accents|Inspirational & Humor"
    
    # Family Life & Home items
    if any(keyword in sentiment for keyword in [
        "happy place", "love you", "love is patient", "home sweet home", "welcome friends"
    ]) or any(keyword in combined_text for keyword in [
        "family", "home", "mother", "grandma", "mom", "daughter"
    ]):
        return "(All) Carson Home Accents|Family Life & Home"
    
    # General decorative items (Everyday Decor as fallback)
    if any(keyword in combined_text for keyword in [
        "frame", "wall art", "lantern", "throw", "quilt", "hanger", "mat", "banner", "msg bar", "message bar"
    ]):
        return "(All) Carson Home Accents|Everyday Decor"
    
    # Fallback to Everyday Decor instead of General Gift
    return "(All) Carson Home Accents|Everyday Decor"

# Apply the category assignment
df["Store Categories"] = df.apply(assign_category, axis=1)

# Save the updated dataset
output_file = f"Carson_Home_Accents_buyhere_updated_{uuid.uuid4().hex}.xlsx"
df.to_excel(output_file, index=False)

print(f"Updated dataset saved as {output_file}")