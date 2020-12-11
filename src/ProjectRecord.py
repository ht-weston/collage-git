from glob import glob
import os
from yaml import dump, full_load

import Img
from SiteRecord import SiteRecord


def get_project_yaml_filename(pr):
    """
    :param pr: ProjectRecord
    :return: the filename we should use for this project's yaml file
    """
    return pr.basedir + "key.yml"


def load_project_record_from_yaml(input_file):
    """
    Returns a ProjectRecord parsed from the given YAML input_file
    :param input_file: file name of file to YAML file to open and read from
    :return: the ProjectRecord object parsed from YAML
    """
    f = open(input_file, "r")
    something = full_load(f)
    f.close()

    return something


def write_project_record_to_yaml(project_record, output_file):
    """
    Writes a ProjectRecord structure out to a YAML file
    :param project_record the ProjectRecord object to write
    :param output_file: the file name to write YAML to
    :return: nothing
    """
    f = open(output_file, "w")
    dump(project_record, f)
    f.close()


class ProjectRecord:
    """
    The ProjectRecord class represents a record of a project. This record contains details relevant to the desired
    production of assets such as the shapefile or the LaTeX document.

    A 'Project' is formed from a root source directory. Within this directory we expect to find 'Site' directories
    containing the relevant images from that site visit.
    """

    def __init__(self, basedir):
        self.project_name = "default project name"
        self.sites = []
        self.basedir = basedir

        if os.path.exists(get_project_yaml_filename(self)):
            self.__dict__.update(load_project_record_from_yaml(get_project_yaml_filename(self)).__dict__)

        self._load_from_folder()

    def _load_from_folder(self):
        """
        Loading from folder -- first we add any new entries from the folder then we remove any entries which
        no longer exist in the directory
        :return:
        """
        self._add_new_from_folder()
        self._remove_missing_from_folder()

    def _add_new_from_folder(self):
        """
        Add new entries to this structure as they are found in the directory.
        :return:
        """
        dirs = glob(os.path.join(self.basedir, "*", ""))

        for d in dirs:
            if d not in [x.directory for x in self.sites]:
                print("found new dir")
                self.sites.append(SiteRecord(d))
            else:
                for site in self.sites:
                    if site.directory == d:
                        site._load_from_folder()

    def _remove_missing_from_folder(self):
        """
        Remove entries in this structure which no longer have representation in the directory
        :return:
        """
        dirs = glob(os.path.join(self.basedir, "*", ""))

        for site in self.sites:
            if site.directory not in dirs:
                self.sites.remove(site)

    def __str__(self):
        """
        Get a string representation
        :return: string representation of this ProjectRecord
        """
        base = "project: \n"

        for site in self.sites:
            base += str(site)

        return base


class ProjectPrinter:
    """
    ProjectPrinter base class. interface exposed is write_to_file
    """
    def __init__(self, project_record, output_filename):
        self.project_record = project_record
        self.output_filename = output_filename

    def write_to_file(self):
        """
        This is an inherited method. Any ProjectPrinter will have a write_to_file method.
        :return: nothing
        """
        output_file = open(self.output_filename, "w")

        sites = self.project_record.sites
        for site in sites:
            if site.include:
                output_file.write(self._handle_site(site))

        output_file.close()


class ShapefileProjectPrinter(ProjectPrinter):
    """
    ShapefileProjectPrinter--Write a Project's shapefile output
    """
    def __init__(self, project_record, output_file):
        ProjectPrinter.__init__(self, project_record, output_file)
        self.image_num = 1

    def _handle_site(self, site):
        """
        Handle a site for shapefile printing
        :param site: the site to print out to shapefile
        :return: string representation of this site to print to the shapefile
        """
        photos = list(filter(lambda x: True if x.include else False, site.images))
        the_string = ""

        for photo in photos:
            the_im = Img.img(photo.image_path)
            the_string += "%s, %s, %s, %s, %s\n" % (the_im.path, the_im.name, the_im.gpsLati, the_im.gpsLong, self.image_num)
            self.image_num += 1

        return the_string


class LatexProjectPrinter(ProjectPrinter):
    """
    LatexProjectPrinter--Write a Project's LaTeX image listing
    """
    _MAX_ROW_IMAGES = 2
    _MAX_WIDTH = 6.2
    _IMAGE_WIDTH = _MAX_WIDTH / _MAX_ROW_IMAGES

    def __init__(self, project_record, output_file):
        ProjectPrinter.__init__(self, project_record, output_file)

    def _handle_row_of_figures(self, row):
        """
        Handle row of figures
        :param row: list of ImageRecords
        :return:  string representation of figure list line for LaTeX
        """
        the_string = "\\InsertRowOfFigures{\\linewidth}{" + str(LatexProjectPrinter._IMAGE_WIDTH) + "in}{2.5in}{m}{"
        the_string += ",".join([x.image_path for x in row])
        the_string += "}\n"

        return the_string

    def _handle_captions(self, row, start_num):
        """
        Handle captions for the entry
        :param row: a list of ImageRecords
        :param start_num: the starting number for these captions
        :return: string representation for the row of captions
        """
        the_string = "\\InsertCaptions["
        the_string += ",".join(["Fig:\\theimsection." + str(x) for x in range(start_num, start_num + len(row))])
        the_string += "]{"
        the_string += ",".join(x.caption for x in row)
        the_string += "}{t}{figure}"

        return the_string

    def _handle_site(self, site):
        """
        Handle a site entry to LaTeX
        :param site: the particular site to handle
        :return: string representation for this site
        """
        photos = list(filter(lambda x: True if x.include else False, site.images))

        num_files = len(photos)
        if num_files == 0:
            # site has no photos, do not include
            return

        the_string = "\n\n\section*{%s}\n\\refstepcounter{imsection}\n" % site.alias

        rows = [photos[i:i + LatexProjectPrinter._MAX_ROW_IMAGES] for i in range(0, num_files, LatexProjectPrinter._MAX_ROW_IMAGES)]

        counter = 1
        for row in rows:
            the_string += "\n\\noindent\n\\begin{minipage}{\\linewidth}\n\\begin{InsertImages}\n"
            the_string += self._handle_row_of_figures(row)
            the_string += self._handle_captions(row, counter)
            the_string += "\\end{InsertImages}\n\\end{minipage}\n\n"
            counter += len(row)

        the_string += "\\pagebreak\n"

        return the_string
