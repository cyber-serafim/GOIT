import os
import sys
import shutil

def show_all_rootdir(rootdir, all_files):
    for it in os.scandir(rootdir):
        if it.is_file():
            all_files.append(it)
        elif it.is_dir():
            show_all_rootdir(it, all_files)
    return all_files

def create_folders_in_rootdir(rootdir, dir_category_dict):
    for key in dir_category_dict.keys():
        os.makedirs(os.path.join(rootdir, key), exist_ok=True)
    os.makedirs(os.path.join(rootdir, 'uknown_extension'), exist_ok=True)

def normalize(name):
    CYRILLIC= "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    LATIN = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    CONVERT = {}
    new_name = ''
    for c, t in zip(CYRILLIC, LATIN):
        CONVERT[ord(c.lower())] = t.lower()
        CONVERT[ord(c.upper())] = t.upper()
    for i in name[:name.rfind('.')]:
        if ord(i) in CONVERT.keys():
            new_i = i.translate(CONVERT)
        elif i.isdigit() or i.isalpha():
            new_i = i
        else:
            new_i = '_'
        new_name = new_name+new_i
    new_name = new_name+name[name.rfind('.'):]
    return new_name

def norm_files_folders_in_arch(rootdir):
    for it in os.scandir(rootdir):
        if it.is_file():
            os.rename(it, os.path.join(rootdir, normalize(it.name)))
        elif it.is_dir():
            norm_files_folders_in_arch(it)
            os.rename(it, os.path.join(
                rootdir, normalize(os.path.basename(it))))


def mv_norm_unarch_files_to_folders(rootdir, dict_extentions, lst_all_files):
    for file in lst_all_files:
        is_moved = False
        for key, value in dict_extentions.items():
            if file.name[(file.name).rfind('.')+1:].upper() in value and key != 'archives':
                shutil.move(file, os.path.join(
                    rootdir, key, normalize(file.name)))
                is_moved = True
                dict_fact_files[key].append(normalize(file.name))
            elif file.name[(file.name).rfind('.')+1:].upper() in value and key == 'archives':
                shutil.unpack_archive(
                    file, os.path.join(rootdir, key, normalize(file.name[:(file.name).rfind('.')])))
                is_moved = True
                dict_fact_files[key].append(normalize(file.name))
        if is_moved == False:
            shutil.move(
                file, os.path.join(rootdir, 'uknown_extension', normalize(file.name)))
            dict_fact_files['uknown_extension'].append(normalize(file.name))


def rm_unnecessary_folders(rootdir):
    for it in os.scandir(rootdir):
        if it.is_dir() and it.name not in dict_extentions.keys() and it.name != 'uknown_extension':
            shutil.rmtree(it, ignore_errors=True)


def validate_correct_path():
    try:
        rootdir = sys.argv[1]
    except IndexError:
        sys.exit('Write path')
    if not os.path.exists(rootdir):
        sys.exit('Uknown directory, write correct directory')


def print_in_console(dict_fact_files, dict_known_unknown_extentions):
    for key, value in dict_fact_files.items():
        print(f"files in cat '{key}': {', '.join(value)}")
        if key == 'uknown_extension':
            dict_known_unknown_extentions['unknown extensions'].update(
                i[(i).rfind('.'):].lower() for i in value)
        else:
            dict_known_unknown_extentions['known extensions'].update(
                i[(i).rfind('.'):].lower() for i in value)
    for key, value in dict_known_unknown_extentions.items():
        print(f"{key}: {', '.join(value)}")


def main():
    validate_correct_path()
    rootdir = sys.argv[1]
    lst_all_files = []
    lst_all_files = show_all_rootdir(rootdir, lst_all_files)
    create_folders_in_rootdir(rootdir, dict_extentions)
    mv_norm_unarch_files_to_folders(
        rootdir, dict_extentions, lst_all_files)
    norm_files_folders_in_arch(
        os.path.join(rootdir, 'archives'))
    rm_unnecessary_folders(rootdir)
    print_in_console(dict_fact_files, dict_known_unknown_extentions)


if __name__ == '__main__':
    dict_extentions = {'archives': ['ZIP', 'GZ', 'TAR'], 'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
                       'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                       'images': ['JPEG', 'PNG', 'JPG', 'SVG'], 'video': ['AVI', 'MP4', 'MOV', 'MKV']} 
                       
    dict_fact_files = {'archives': [],  'audio': [], 'documents': [], 
                      'images': [], 'uknown_extension': [], 'video': []}

    dict_known_unknown_extentions = {
        'known extensions': set(), 'unknown extensions': set()}
    main()