"""Merging G2P dictionaries"""

import os
import codecs


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


def merge_dict(to_merge: list, final_dict_name: str) -> None:
    """Merge the dictionaries in to_merge and name it final_dict_name"""

    if (no_forbidden_characters(final_dict_name) and
            not file_exists_but_shouldnt(final_dict_name) and
            all([file_exists(this_file) for this_file in to_merge])):

        all_dict_entries = []
        for this_file in to_merge:
            with codecs.open(this_file, "r", encoding="utf-8") as current_dict:
                current_dict_entries = current_dict.read()

            old_list_current_dict_entries = current_dict_entries.split("\n")
            new_list_current_dict_entries = [entry for entry in old_list_current_dict_entries if entry != '']
            all_dict_entries.extend(new_list_current_dict_entries)

        all_dict_entries.sort()
        new_dict_file_content = "\n".join(all_dict_entries)
        with codecs.open(final_dict_name, 'w', encoding="utf-8") as new_dict_file:
            new_dict_file.write(new_dict_file_content)

        print("Success!")


if __name__ == '__main__':
    done = False
    to_merge = []

    while not done:
        this_dict = input("Enter the name of a dictionary for the merging (or Q to stop): ")
        if this_dict == "Q" or this_dict == "q":
            done = True
        else:
            to_merge.append(this_dict + ".dict")

    if to_merge == []:
        print("No dictionary entered!")
    else:
        final_dict_name = input("Enter the name of the final dictionary: ")
        merge_dict(to_merge, final_dict_name + '.dict')
