import os
import pickle
# c.get_all_sample_identifier , sollte leere liste liefern wenn keine daten (sonst input_data = ())
# beachten bei identifiezierer erstellen: immer mit komma am ende (+kommentierung warum), immer feste länge, dazu username begrenzen!

#schreiben: erst in datei mit allen namen zu dic hizufügen (key identifier - value filename)
#auslesen: try catch alle dic zusammenfügen wenn key doppelt ersetzen durch (1)

sample_files_list = []
sample_overview_files_list = []
path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Data'))

def fill_all_filelists():
    if not sample_overview_files_list:
        # noch nicht befüllt
        directory_list = os.listdir(path)
        for f in directory_list:
            if f.startswith("Overview_"):
                sample_overview_files_list.append(f)
            else:
                sample_files_list.append(f)

def write_sample_to_file (sample):
    fill_all_filelists()
    sample_filename = sample.create_file_name()
    sample_identifier = sample.get_short_identifier()

    # add new filename to dictionary in overview file
    if not sample_overview_files_list:
        # no overview file, set new file name
        new_overview_filename = "Overview_" + sample_filename
        # create new file
        with open (path + "\\" + new_overview_filename, "bw") as file:
            pickle.dump({sample_identifier : sample_filename}, file)
        sample_overview_files_list.append(new_overview_filename)
    else:
        try:
            with open (path  + "\\" + sample_overview_files_list[0], "rb") as file:
                samples_overview = pickle.load(file)
                samples_overview[sample_identifier] = sample_filename
            with open (path  + "\\" + sample_overview_files_list[0], "bw") as file:
                pickle.dump(samples_overview, file)
        except EOFError:
            # file is empty
            with open (path  + "\\" + sample_overview_files_list[0], "bw") as file:
                pickle.dump({sample_identifier : sample_filename}, file)

    # create new file
    with open (path  + "\\" + sample_filename, "bw") as file:
            pickle.dump(sample, file)

# hinzufügen: error handling wenn es files nicht gibt, wenn files leer sind

def read_sample_identifier_from_file():
    fill_all_filelists()

def read_samples_from_file():
    fill_all_filelists()

