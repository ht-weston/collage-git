from ImageRecord import ImageRecord
import os


class SiteRecord:
    """
    The SiteRecord class represents a record of a site. This record contains details relevant to the site observations.

    A 'SiteRecord' is formed from a root site source directory. Within this directory we expect to find image
    observations taken at the given site.
    """

    def __init__(self, the_dir):
        """
        :param the_dir: directory name for site, includes trailing /
        """
        self.directory = the_dir
        self.include = True
        self.images = []
        self._load_from_folder()
        self.alias = self._get_site_alias()

    def _get_site_alias(self):
        """
        A site can have an 'alias' or nickname / shorthand name for the site which may be useful to the reader
        :return: string representing the alias to be used for the site
        """
        return os.path.basename(os.path.split(self.directory)[0])

    def _load_from_folder(self):
        """
        This is how we keep a SiteRecord in sync with the folder.
        First we add any new directories found on the filesystem into the data structure.

        Then we check to see if there are any entires in the data structure whose representative files have since been
        removed from the filesystem
        :return: nothing
        """
        self._add_new_from_folder()
        self._remove_missing_from_folder()

    def _add_new_from_folder(self):
        """
        Add new images found in directory which are non existent in the site
        :return: none
        """
        count = len(self.images) + 1

        for file in [os.path.join(self.directory, x) for x in os.listdir(self.directory)]:
            if file not in [x.image_path for x in self.images]:
                self.images.append(ImageRecord(count, file))
                count += 1

        self.images.sort()

    def _remove_missing_from_folder(self):
        """
        Remove images from the structure which are no longer found in the directory
        :return: none
        """
        for image in self.images:
            if not os.path.exists(image.image_path):
                self.images.remove(image)

    def __str__(self):
        """
        Get a string representation of this site
        :return:
        """
        base = "site: " + self.alias + "\n"

        for x in self.images:
            base += str(x)

        return base
