from os import listdir, getcwd, makedirs
from os.path import exists, isdir, join


def verify_parallel_filenames(img_set):
    # directories = get_img_sets()
    directories = img_set
    # check if filenames are parallel for two dirs
    not_parallel = []
    parallel = []

    for dir1 in directories.keys():
        for dir2 in directories.keys():
            if dir1 == dir2:
                continue

            if directories[dir1] != directories[dir2]:
                if (dir1,dir2) not in not_parallel and (dir2,dir1) not in not_parallel:
                    print('\nWarning: {} and {} directories are NOT PARALLEL!'.format(dir1,dir2))
                    not_parallel.append((dir1,dir2))
            else:
                if (dir1,dir2) not in parallel and (dir2,dir1) not in parallel:
                    print('\nYAY!, {} and {} directories are PARALLEL!'.format(dir1,dir2))
                    parallel.append((dir1,dir2))
    return parallel, not_parallel

def get_img_dir(rel_dir='/images/'):
    canon_dir = getcwd() + rel_dir
    # print('data directory:\n     {}'.format(canon_dir))
    return canon_dir

def get_subdirs(canon_dir=get_img_dir(), print_subdirectories=False):
    directories = [ name for name in listdir(canon_dir) if isdir(join(canon_dir, name)) ]

    if print_subdirectories == True:
        print('\nsubdirectories: \n     {}'.format(directories))
    
    return directories

def get_img_sets(canon_dir=get_img_dir(), print_subdirectories=False):
    directories = [ name for name in listdir(canon_dir) if isdir(join(canon_dir, name)) ]

    if print_subdirectories == True:
        print('\nsubdirectories: \n     {}'.format(directories))

    image_set_filenames = dict()

    # preserve only .jpg images
    for directory in directories:
        file_list = listdir(canon_dir + directory)
        file_list = [filename for filename in file_list if '.jpg' in filename]
        image_set_filenames[directory] = file_list
        
    return image_set_filenames#color_img_filenames, thermal_img_filenames

def create_dir(directory, to_create):
    if not exists(directory + to_create):
        makedirs(directory + to_create)
