import os
import pickle
# c.get_all_sample_identifier , sollte leere liste liefern wenn keine daten (sonst input_data = ())
# beachten bei identifiezierer erstellen: immer mit komma am ende (+kommentierung warum), immer feste länge, dazu username begrenzen!

#auslesen: try catch alle dic zusammenfügen wenn key doppelt ersetzen durch (1)

sample_files_list = []
overview_files_list = []
identifier_and_filenames = {}
path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Data'))

# initialize lists if not already done
def fill_all_filelists():
    if not overview_files_list:
        # noch nicht befüllt
        directory_list = os.listdir(path)
        for f in directory_list:
            if f.startswith("Overview_"):
                overview_files_list.append(f)
            else:
                sample_files_list.append(f)

def write_sample_to_file (sample):
    fill_all_filelists()
    sample_filename = sample.create_file_name()
    sample_identifier = sample.get_short_identifier()

    # add new filename to dictionary in overview file
    if not overview_files_list:
        # no overview file, set new file name
        new_overview_filename = "Overview_" + sample_filename
        # create new file
        with open (total_path(new_overview_filename), "bw") as file:
            pickle.dump({sample_identifier : sample_filename}, file)
        overview_files_list.append(new_overview_filename)
    else:
        try:
            with open (total_path(overview_files_list[0]), "rb") as file:
                samples_overview = pickle.load(file)
                samples_overview[sample_identifier] = sample_filename
            with open (total_path(overview_files_list[0]), "bw") as file:
                pickle.dump(samples_overview, file)
        except EOFError:
            # file is empty
            with open (total_path(overview_files_list[0]), "bw") as file:
                pickle.dump({sample_identifier : sample_filename}, file)

    # create new file
    with open (total_path(sample_filename), "bw") as file:
            pickle.dump(sample, file)

# hinzufügen: error handling wenn es files nicht gibt, wenn files leer sind

def read_sample_identifier_from_file():
    fill_all_filelists()
    global identifier_and_filenames
    for f in overview_files_list:
        try:
            with open (total_path(f), "rb") as file:
                identifier_and_filenames |= pickle.load(file)
        except:
            # file is empty or not correct filled (broken)
            os.remove(total_path(f))
    return list(identifier_and_filenames.keys())
            

def read_samples_from_files(identifier_list):
    samples = []
    for i in identifier_list:
        with open (total_path(identifier_and_filenames[i]), "rb") as file:
            samples.append(pickle.load(file))
    return samples


def total_path(filename):
    return os.path.join(path, filename)

# evtl. methode wie "remove_broken_data", die file löscht und verweis in overview entfernt, jeweils in try catch block, diese methode dann als handling

