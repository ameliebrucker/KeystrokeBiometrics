import os
import pickle

sample_files_list = []
overview_files_list = []
# dictionary with identifier and filename per sample
identifier_and_filenames = {}
# path for data directory
path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))

def total_path(filename):
    """
    forms total path out of path for data directory and filename

    Parameter:
    filename: filename for the total path

    Return:
    total path including filename
    """

    return os.path.join(path, filename)

def fill_filelists():
    """
    fills overview_files_list and sample_files_list with file names from directory if not already done

    Precondition:
    overview_files_list and sample_files_list are initialized
    """

    if not overview_files_list:
        # lists are empty, get names of all files in directory
        directory_list = os.listdir(path)
        for f in directory_list:
            # put names of files with sample overview in overview_files_list
            if f.startswith("Overview_"):
                overview_files_list.append(f)
            # put names of files with single samples in sample_files_list
            else:
                sample_files_list.append(f)

def write_sample_to_file (sample):
    """
    writes sample to new binary file and adds file name and sample identifier to sample overview file

    Parameter:
    sample: sample, which should be archived

    Precondition:
    overview_files_list and sample_files_list are initialized
    """

    fill_filelists()
    sample_filename = sample.get_file_name()
    sample_identifier = sample.get_short_identifier()
    # add filename for new sample to dictionary in overview file
    if not overview_files_list:
        # no overview file exists, create new one
        new_overview_filename = "Overview_" + sample_filename
        overview_files_list.append(new_overview_filename)
        overview_filename = new_overview_filename
        # set current sample as first entry in new overview dictionary
        overview_dic = {sample_identifier : sample_filename}
    else:
        overview_filename = overview_files_list[0]
        try:
            # get overview dictionary from file
            with open (total_path(overview_filename), "rb") as file:
                overview_dic = pickle.load(file)
                # add current sample to overview dictionary
                overview_dic[sample_identifier] = sample_filename
        except:
            # overview file is empty or not correct filled, create new dictionary
            overview_dic = {sample_identifier : sample_filename}
    # write dictionary in overview file
    with open (total_path(overview_filename), "bw") as file:
        pickle.dump(overview_dic, file)
    # create new file with sample
    with open (total_path(sample_filename), "bw") as file:
        pickle.dump(sample, file)
    sample_files_list.append(sample_filename)

def read_sample_identifier_from_file():
    """
    provides all sample identifiers from overview files, corrects them if files were deleted and fills identifier_and_filenames

    Return:
    list of all sample identifiers

    Precondition:
    overview_files_list and sample_files_list are initialized
    """

    fill_filelists()
    global identifier_and_filenames
    # combine all dictionaries from overview files
    for f in overview_files_list:
        try:
            with open (total_path(f), "rb") as file:
                dict_from_file = pickle.load(file)
            # check if sample files which are listed in overview were deleted
            dict_for_file = dict (dict_from_file)
            for k, v in dict_from_file.items():
                if v not in sample_files_list:
                    # sample no longer exists, delete from overview
                    del dict_for_file[k]
            dict_for_file_len = len(dict_for_file)
            if len(dict_from_file) > dict_for_file_len:
                # there were deleted files
                if dict_for_file_len == 0:
                    # all samples from overview were deleted
                    os.remove(total_path(f))
                    overview_files_list.remove(f)
                else:
                    with open (total_path(f), "bw") as file:
                        # write corrected dictionary to file
                        pickle.dump(dict_for_file, file)
            identifier_and_filenames |= dict_for_file
        except:
            # file f is empty or not correct filled (broken)
            os.remove(total_path(f))
            overview_files_list.remove(f)
            print (f"Overview file \"{f}\" was broken, it was removed.")
    return list(identifier_and_filenames.keys())
            

def read_samples_from_files(identifier_list):
    """
    provides samples for given identifiers

    Parameter:
    identifier_list: list of identifiers for which a sample should be returned

    Return:
    samples which belong to given identifiers as list

    Precondition:
    overview_files_list and sample_files_list are initialized
    identifier_and_filenames is filled (read_sample_identifier_from_file() was executed)
    """

    samples = []
    for i in identifier_list:
        try:
            # read sample from each file, which belongs to identifier
            with open (total_path(identifier_and_filenames[i]), "rb") as file:
                samples.append(pickle.load(file))
        except:
            # check if broken file was already removed
            if i in identifier_and_filenames.keys():
                # remove broken file
                # sample will also be removed from overview during next call of read_sample_identifier_from_file() 
                os.remove(total_path(identifier_and_filenames[i]))
                sample_files_list.remove(identifier_and_filenames[i])
                del identifier_and_filenames[i]
                print (f"File for sample \"{i}\" was broken, it was removed.")

    return samples