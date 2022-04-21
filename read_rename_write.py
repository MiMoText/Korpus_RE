import glob
import os

# by KD
# Vorlage für die üblichen Input-/Output-Operationen


filelist = glob.glob("../data_in/example_file*.txt")
for file in filelist:
    try:
        f = open(file, encoding="utf-8")
    except:
        print("File not found or not readable.")
        continue

    full_text = f.read()
    print(file)
    print(full_text)
    f.close()


    # Rename edited file
    for edited_file in filelist:
        my_basename = os.path.basename(file)
    my_basename_split = os.path.splitext(my_basename)
    my_fileending = my_basename_split[1]
    my_basename_split = my_basename_split[0]

    # after file has been edited write file out with additional ending "edited".
    new_filename = "".join([my_basename_split, "_edited", my_fileending])

    print(new_filename)

    file_out = open("../data_out/" + new_filename, "w", encoding="utf-8")
    file_out.write(full_text)
    file_out.close()

print(len(filelist))
# file output after editing


# todo hier stimmt noch iwas mit der schleife nicht
# es wird nur file2 geschreiben, file1 fehlt





