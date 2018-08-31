"""Creating a dictionary containing the phonemic transcription of the words OOV (out of vocabulary)
 after an attempt to run the Montreal Forced Aligner"""

import os
import codecs

SOUND_TO_LETTERS = {'p': 'p', 't': 't', }
VOWELS = {'A', 'E', 'I', 'O', 'U', 'Y'}  # Note that y is a vowel here
CONSONANTS = {chr(x) for x in range(65, 91)} - VOWELS
PROPER_NOUNS_TO_PHON = {'BIYONG': 'b i j N', 'NGUIDJOL': 'g i Z o l', 'NGO': 'n g o',
                        'BILONG': 'b i l N', 'MINLEND': 'm i l i n d', 'FOUDA': 'f u l a', 'OMGBA': 'u m b a'}


def file_exists(this_file: str) -> bool:
    """Check whether this_file exists (it should)"""
    if not os.path.isfile(this_file):
        print("\n")
        print("{} does not exist.".format(this_file))
        print("Please make sure you typed the name of the file correctly and that you are in the correct"
              " directory.\n")
        return False
    else:
        return True


def file_exists_but_shouldnt(this_file: str) -> bool:
    """Check whether this_file exists (it shouldn't)"""
    if os.path.isfile(this_file):
        print("\n")
        print("{} already exists.".format(this_file))
        print("Please choose another name or delete the existing file.\n")
        return True
    else:
        return False


def no_forbidden_characters(this_new_item: str) -> bool:
    """Check whether this_new_item (file or folder) contains no forbidden characters"""
    forbidden_characters = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    folder_name_wrong = any([char in forbidden_characters for char in this_new_item])
    if folder_name_wrong:
        print("\nYou cannot use the following characters in your file name:\n")
        print(', '.join(forbidden_characters) + '\n')
        return False
    else:
        return True


def generate_dict(oov_file_name: str, original_dict_file_name: str, new_dict_file_name: str) -> None:
    """Generate a dictionary from oov_file_name"""

    if (file_exists(oov_file_name) and
            file_exists(original_dict_file_name) and
            not file_exists_but_shouldnt(new_dict_file_name) and
            no_forbidden_characters(new_dict_file_name)):

        # Read oov file
        with codecs.open(oov_file_name, "r", encoding="utf-8") as oov_file:
            all_oovs = oov_file.read()

        old_list_of_oovs = all_oovs.replace("\r", "").split("\n")
        # Get rid of empty string. Make uppercase to facilitate comparisons.
        list_of_oovs = [oov.upper() for oov in old_list_of_oovs if oov != '']

        # Read original dictionary
        with codecs.open(original_dict_file_name, "r", encoding="utf-8") as original_dict:
            all_dict_entries = original_dict.read()

        list_of_dict_entries = all_dict_entries.split("\n")

        original_word_to_sound = {}

        for entry in list_of_dict_entries:
            if entry != '':  # Get rid of empty string
                first_space_index = entry.index(" ")
                word = entry[:first_space_index]
                sound = entry[first_space_index+1:]
                original_word_to_sound[word] = sound

        new_word_to_sound = {}
        new_word_to_sound_unsure = {}
        what_to_do = {}
        for oov in list_of_oovs:

            # SURE
            # The oov is a proper noun that whose phonetic transcription cannot be guessed by the code further below
            if oov in PROPER_NOUNS_TO_PHON:
                new_word_to_sound[oov] = PROPER_NOUNS_TO_PHON[oov]

            # SURE
            # The oov actually consists of 2 known words connected by an apostrophe
            elif "'" in oov:
                apostrophe_index = oov.index("'")
                first_part = oov[:apostrophe_index+1]
                second_part = oov[apostrophe_index+1:]
                parts_found = first_part in original_word_to_sound and second_part in original_word_to_sound

                if parts_found:
                    sound = original_word_to_sound[first_part] + " " + original_word_to_sound[second_part]
                    new_word_to_sound[oov] = sound

            # NOT SURE
            # Completely new word
            else:

                char_to_sound = {'a': 'a', 'b': 'b', 'c': 'k', 'd': 'd', 'e': 'e', 'é': 'e', 'è': 'e', 'f': 'f',
                                   'g': 'g', 'h': '', 'i': 'i', 'j': 'Z', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n',
                                   'o': 'o', 'p': 'p', 'q': 'k', 'r': 'R', 's': 's', 't': 't', 'u': 'y', 'v': 'v',
                                   'w': 'w', 'x': 'k s', 'y': 'j', 'z': 'z', 'œ':'neuf',
                                 '1':'1', '2':'2', '3':'3','4':'4','5':'5','6':'6','7':'7','8':'8', '9':'9','0':'0'}
                # Note h and numbers must be amended
                # œ is used here but it is preferrable to replace œ by oe in GenerateLab.py itself

                # SURE
                # Single character not stored in the original dictionary
                already_found_one_char = False
                sounds_in_oov = []

                if len(oov) == 1:
                    one_char_to_sound = {'H': 'a S', 'P': 'p e', 'R': 'E R'}
                    if oov in one_char_to_sound:
                        sounds_in_oov.append(one_char_to_sound[oov])
                        already_found_one_char = True

                characters = list(oov)
                length = len(characters)
                last_index = length - 1
                i = 0

                # Iterate over each character (might skip some if needed)
                while not already_found_one_char and i < length:
                    char = characters[i]

                    # Just to silence PyCharm
                    next_char = None
                    further_char = None

                    if i < last_index:
                        next_char = characters[i+1]
                        if i < last_index - 1:
                            further_char = characters[i+2]

                    # Yaoundé
                    if char == 'O' and i < last_index and (next_char == 'O' or next_char == 'U'):
                        sound_unit = 'u'
                        i += 1
                    # Suzanne
                    elif char == 'N' and (i == last_index - 2) and (next_char == 'N' and further_char == 'E'):
                        sound_unit = 'n'
                        i += 2
                    # Rachel
                    elif char == 'C' and i < last_index and next_char == 'H':
                        sound_unit = 'S'
                        i += 1
                    # Samuel
                    elif char == 'U' and i < last_index and next_char == 'E':
                        sound_unit = 'huit E'
                        i += 1
                    # MANGUÈLÈ, NGUÈNÈ
                    elif char == 'U' and i < last_index and next_char == 'È':
                        sound_unit = 'e'
                        i += 1
                    # Cicam, cependant. The second case is very unlikely though
                    elif char == 'C' and i < last_index and (next_char == 'I' or next_char == 'E'):
                        sound_unit = 's'  # Don't skip characters here
                    # Nguidjol
                    elif char == 'U' and i < last_index and next_char == 'I':
                        sound_unit = 'i'
                        i += 1
                    # KELLÉ
                    elif char == 'L' and i < last_index and next_char == 'L':
                        sound_unit = 'l'
                        i += 1
                    # Mbock
                    elif char == 'C' and i < last_index and next_char == 'K':
                        sound_unit = 'k'
                        i += 1
                    # Likeng, Nyong, Bakang, Libong
                    elif char in VOWELS and (i == last_index - 2) and next_char == 'N' and further_char == 'G':
                        vowel_to_sound = {'A': 'a', 'E': 'E', 'I': 'i', 'O': 'O', 'U': '', 'Y': ''}
                        # U and Y are left empty because we don't have such data (yet)

                        sound_unit = vowel_to_sound[char] + ' G'
                        i += 2
                    # M and N are not pronounced if they are the first letter and followed by a consonant
                    elif (char == 'M' or char == 'N') and i < last_index and i == 0 and next_char in CONSONANTS:
                        sound_unit = char_to_sound[next_char.lower()]
                        i += 1
                    else:
                        sound_unit = char_to_sound[char.lower()]

                    # Add the sound to the list
                    sounds_in_oov.append(sound_unit)
                    i += 1
                whole_oov_sound = " ".join(sounds_in_oov).replace('  ', ' ')  # Remove double spaces (for h)

                if oov in ['D', 'J', 'L', 'M', 'N', 'QU', 'S', 'Y']:
                    what_to_do[oov] = whole_oov_sound
                else:
                    if already_found_one_char:
                        new_word_to_sound[oov] = whole_oov_sound
                    else:
                        new_word_to_sound_unsure[oov] = whole_oov_sound

        print("Original list of oovs ({}):\n{}".format(len(list_of_oovs), list_of_oovs))
        print('\n')
        print("Words identified for sure ({}):\n{}".format(len(new_word_to_sound), new_word_to_sound))
        print('\n')
        print("Words guessed ({}):\n{}".format(len(new_word_to_sound_unsure), new_word_to_sound_unsure))
        print('\n')
        print("What to do? ({}):\n{}".format(len(what_to_do), what_to_do))
        print('\n')
        # not_found = list(set(list_of_oovs) - set(new_word_to_sound.keys()))
        # print('Words not identified ({}):\n{}'.format(len(not_found), not_found))

        new_dict_file_list = []
        for word in new_word_to_sound:
            new_dict_file_list.append(word + ' ' + new_word_to_sound[word])

        for word in new_word_to_sound_unsure:
            new_dict_file_list.append(word + ' ' + new_word_to_sound_unsure[word])

        new_dict_file_content = "\n".join(new_dict_file_list)
        with codecs.open(new_dict_file_name, 'w', encoding="utf-8") as new_dict_file:
            new_dict_file.write(new_dict_file_content)


if __name__ == '__main__':
    oov_file_name = input("Enter the name of the file containing the OOVs: ")
    original_dict_file_name = input("Enter the name of the original dictionary: ")
    new_dict_file_name = input("Enter the name of the new dictionary to contain the oovs: ")
    generate_dict(oov_file_name + ".txt", original_dict_file_name + '.dict', new_dict_file_name + '.dict')
