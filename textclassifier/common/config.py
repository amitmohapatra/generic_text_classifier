__author__ = 'amitkum'

from os import sep, path, makedirs
from gc import collect, garbage

from collections import namedtuple


class Config(object):
    """
    Make all resources related entity to object.
    """

    def __init__(self, project_env):
        self.base_dir = path.dirname(path.dirname(path.dirname(path.dirname(path.dirname(path.dirname(__file__))))))
        self.project_env = project_env
        self.setup = self.__setup()

    def __setup(self):
        """
        :param project_env: environment type (prod, test, local)
        :return: None
        #read the config from respective folder.
        """
        try:
            config_path = self.__create_config_file_if_not_exist(
                sep.join(["resource", "%s" % self.project_env, "config"]))
            name, val = self._read_config_file(config_path)
            return self.__create_namedtuple(name, val)
        except Exception, e:
            raise Exception("Config : Error while reading config : %s" % e.message)

    def __create_config_file_if_not_exist(self, relative_path):
        """
        :param relative_path: relative path of config file
        :return: None
        #if config file not present then create config file in respective setup directory.
        """
        try:
            config_file_path = "%s%s%s" % (self.base_dir, sep, relative_path)
            if not path.exists(config_file_path):
                f = open(config_file_path, "w")
                f.close()
                raise
        except Exception:
            raise Exception("Empty config file with required config lines  created in directory : %s : under resource\n"
                            "please fill the requirements in the file before proceed, please follow the commented\n"
                            "line in the file. Else contact the developer Amit in amit.ricky1989@gmail.com for more "
                            "info" % self.project_env)

    def _read_config_file(self, file_path):
        """
        :param file_path: absolute path of the file.
        :return: entity name and value as list inside config file.
        """
        val = []
        name = []

        with open(file_path, 'r') as f:

            for l in f:
                if l != "\n" and l:
                    # if any name started with #, consider as comment
                    check_comment = "#"
                    if l.startswith(check_comment):
                        continue

                    # to separate the key and value
                    line = l.split("=")
                    name.append(line[0].strip().lower())

                    if line[1].strip().lower() == 'true':
                        val.append(True)
                    elif line[1].strip().lower() == 'false':
                        val.append(False)
                    elif (len(line[1].strip().lower()) == 0) or (line[1].strip().lower() == "none"):
                        val.append(None)
                    else:
                        if line[0].strip().lower() in ["gcs_credential_path", "local_xml_result", "index_files_path",
                                                       "log_path"]:
                            self.__create_dir(line[1].strip())
                        val.append(line[1].strip())
            f.close()
        return name, val

    def __create_namedtuple(self, name, val):
        """
        :param name: name list
        :param val: corresponding value list
        :return: namedtuple
        """
        try:
            named_object = namedtuple('NAMED_OBJECT', ",".join(name))
            return named_object._make(val)
        except Exception, e:
            raise Exception("Config : Error while named tupple created : %s" % e.message)

    def __create_dir(self, local_path):
        """
        :param relative_path: relative path of directory
        :return: None
        #if directory does not exists , create directory
        """
        try:
            if not path.exists(local_path):
                makedirs(local_path)
            return local_path
        except Exception, e:
            raise Exception("Config : Unable to create diractory : %s" % e.message)

    def terminate(self):
        """
        :return: None
        # delete everything from self, so that using this object fails results
        # in an error as quickly as possible
        """

        try:
            for val in self.__dict__.keys():
                try:
                    delattr(self, val)
                except:
                    pass
        except Exception, e:
            pass

        collect()
        del garbage[:]
