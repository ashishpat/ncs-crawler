import json
import os
import re
import ntr

def clean_text_for_filename(text):
    # Replace spaces with underscores
    text = text.strip()
    
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    text = re.sub(r'[^A-Za-z _-]+', '', text)
    
    # Convert to lowercase for consistency
    text = text.lower()
    
    return text

def clean_text_for_songnumber(text):
    # Replace spaces with underscores
    text = text.strip()
    
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    text = re.sub(r'[^A-Za-z0-9 _-]+', '', text)
    text = re.sub(r's', 'b', text)
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

def line_contains_metadata_nepali(line):
    pattern = re.compile(r'को\.|[\d]+\.')
    match = re.search(pattern, line)
    return match

def line_contains_metadata(line):
    if '[Chorus]' in line:
        return True
    elif '[Verse]' in line:
        return True
    else:
        return False

def add_metadata_for_song(line, filename_prefix):
     if 'c' in filename_prefix:
         cprefix = 'को.'
         line  = f'{cprefix} {line}'
     elif 's' in filename_prefix:
         cprefix = '१.'
         line  = f'{cprefix} {line}'
     else:
         pass
     return line

# Specify the path to the JSON file
jsonl_file_path = 'songs.jsonl'
folder_path = 'song'

# Read the JSON file
with open(jsonl_file_path, 'r', encoding='utf-8') as f:
    for line in f: 
        data = json.loads(line.strip())

        #Make directory if it doesn't exists
        os.makedirs(folder_path, exist_ok=True)

        #Romanize file names so its easier to search
        romanize_title = ntr.nep_to_rom(data['name'])

        #Clean file names 
        cleaned_name = clean_text_for_filename(romanize_title)
        song_number = f"{clean_text_for_songnumber(data['number'])}"
        file_name =  f"{cleaned_name}.txt" if not song_number else f"{song_number} {cleaned_name}.txt"
        file_path = os.path.join(folder_path, file_name)
        
        #Split songs to individual lines
        song_lines = data['song'].splitlines()
        song_line_md = []


        #Format [Chorus] and [Verses]
        for index, line in enumerate(song_lines):
                if (index == 0):
                    if not line_contains_metadata_nepali(line):
                        line = add_metadata_for_song(line, data['number'])
                cleaned_line = convert_metadata_for_songs(line)
                if cleaned_line:
                    splines = cleaned_line.splitlines()
                    for lines in splines:
                        song_line_md.append(lines)
        
        #Write songs to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            for songline in song_line_md:
                if (line_contains_metadata(songline)):
                    f.write(f"{songline.strip()}\n")
                else:
                    #only romanize text other than [Chorus], [Verse]
                    romanize = ntr.nep_to_rom(songline)
                    f.write(f"{songline.strip()}\n{romanize.strip().lower()}\n\n")

