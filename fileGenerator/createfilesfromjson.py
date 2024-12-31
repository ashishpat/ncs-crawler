import json
import os
import re
import ntr

def clean_text_for_filename(text):
    # Replace spaces with underscores
    text = text.strip()
    
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    text = re.sub(r'[^\w\s\-]', '', text)
    
    # Convert to lowercase for consistency
    text = text.lower()
    
    return text

def convert_metadata_for_songs(line):
    line = line.strip()

    line = re.sub(r'को\.', '[Chorus]\n', line)
    line = re.sub(r'[\d]+\.', '[Verse]\n', line)

    return line

def remove_metadata_for_song(line):
    line = line.strip()
    cleaned_text = re.sub(r'\[Chorus\] | \[Verse\]', '', line) 
    return cleaned_text

def line_contains_metadata(line):
    if '[Chorus]' in line:
        return True
    elif '[Verse]' in line:
        return True
    else:
        return False


# Specify the path to the JSON file
jsonl_file_path = 'songs.jsonl'
folder_path = 'song'
# Read the JSON file
with open(jsonl_file_path, 'r', encoding='utf-8') as f:
    for line in f: 
        data = json.loads(line.strip())

        os.makedirs(folder_path, exist_ok=True)
        romanize = ntr.nep_to_rom(data['name'])
        clean_name = clean_text_for_filename(f"{data['number']} {romanize}")            
        file_name = f"{clean_name}.txt"
        file_path = os.path.join(folder_path, file_name)
        
        song_lines = data['song'].splitlines()
        song_line_md = []
        for line in song_lines:
                cleaned_line = convert_metadata_for_songs(line)
                if cleaned_line:
                    splines = cleaned_line.splitlines()
                    for lines in splines:
                        song_line_md.append(lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for songline in song_line_md:
                if (line_contains_metadata(songline)):
                    f.write(f"{songline.strip()}\n")
                else:
                    romanize = ntr.nep_to_rom(songline)
                    f.write(f"{songline.strip()}\n{romanize.strip().lower()}\n\n")

