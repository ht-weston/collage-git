from collections import defaultdict
import os
from Img import img
import yaml
import pprint

MAX_ROW_IMAGES = 2
MAX_WIDTH = 6.2
IMAGE_WIDTH = MAX_WIDTH/MAX_ROW_IMAGES


def get_safe_name(name):
    return name.replace("_", "\\_")


def get_yaml_filename(dir):
    """
    get the name of the yaml index file corresponding to a directory
    :param dir: a directory name, ending in /
    :return:
    """
    return dir + "key.yml"


class DirProcessor:
    def __init__(self, directory):
        self.directory = directory
        self.image_num = 1

    def _get_yaml_name(self):
        return self.directory + "key.yml"

    def _load_yaml_index(self):
        if not os.path.exists(self._get_yaml_name()):
            pass

        yaml_file = open(self._get_yaml_name(), "r+")
        yaml_dict = yaml.load(yaml_file)

        for k, v in yaml_dict.items():
            print(k)
            print(yaml_dict[k])

    def get_images(self):
        img_dict = defaultdict(list)
        for dp, dn, fs in os.walk(self.directory):
            for f in fs:
                try:
                    img_dict[dp].append(img(os.path.join(dp, f)))
                except Exception as e:
                    continue
            img_dict[dp].sort(key=lambda x: x.ctime, reverse=False)
        return img_dict

    def latex_handle_row_of_figures(self, row):
        preamble = "\\InsertRowOfFigures{\\linewidth}{" + str(IMAGE_WIDTH) + "in}{2.5in}{m}{"
        retval = preamble
        retval += ",".join([x.path for x in row])
        retval += "}\n"
        return retval

    def latex_handle_captions(self, row, start_num):
        preamble = "\\InsertCaptions["
        v = preamble
        v += ",".join(["Fig:\\theimsection." + str(x) for x in range(start_num, start_num + len(row))])
        v += "]{"
        v += ",".join(x.name for x in row)
        v += "}{t}{figure}"

        return v

    def latex_handle_section(self, latex_file, folder_name, files_in_folder):
        retval = ""

        if len(files_in_folder) == 0:
            # there are no images in this folder!
            return ""

        retval += "\n\n\section*{%s}\n\\refstepcounter{imsection}\n" % (get_safe_name(os.path.basename(folder_name)))

        num_files = len(files_in_folder)
        rows = [files_in_folder[i:i+MAX_ROW_IMAGES] for i in range(0, num_files, MAX_ROW_IMAGES)]
        counter = 1
        for row in rows:
            retval += "\n\\noindent\n\\begin{minipage}{\\linewidth}\n\\begin{InsertImages}\n"
            retval += self.latex_handle_row_of_figures(row)
            retval += self.latex_handle_captions(row, counter)
            retval += "\end{InsertImages}\n\end{minipage}\n\n"
            counter += len(row)

        retval += "\\pagebreak\n"

        latex_file.write(retval)

    def handle_write_shapefile(self, shape_file, files_in_folder):
        for image_file in files_in_folder:
            shape_file.write("%s, %s, %s, %s, %s\n" % (image_file.path, image_file.name, image_file._gpsLati, image_file.gpsLong, self.image_num))
            self.image_num += 1

    def do_process(self, latex_filename, shape_filename):
        img_dict = self.get_images()

        shape_file = open(shape_filename, "w")
        shape_file.write("file path, file name, latitude, longitude, collage id\n")

        latex_file = open(latex_filename, "w")

        for folder_name, files_in_folder in img_dict.items():
            # this loop iterates once for each of the main folders

            self.handle_write_shapefile(shape_file, files_in_folder)
            self.latex_handle_section(latex_file, folder_name, files_in_folder)

        shape_file.close()
        latex_file.close()

        return
