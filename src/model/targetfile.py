from pathlib import Path

class TargetFile:
    def __init__(self, target_file):
        self.set_target_file(target_file)

    @property
    def get_target_file(self):
        """
        Method returning a value of path
        :return: target file path
        """
        return self.target_file

    def set_target_file(self, target_file):
        """
        Method setting a value of path and checking
         if the target file is really existing and accessible.
        :param target_file: target file path
        """
        if not isinstance(target_file, str):
            raise TypeError("File has to be chosen")
        if not target_file.strip():
            raise FileNotFoundError("Chosen file string is empty")

        path_object = Path(target_file)
        if not path_object.is_file():
            raise FileNotFoundError("Chosen file aint file")

        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                pass
        except PermissionError:
            raise PermissionError("Permission denied")
        except OSError:
            raise OSError("System error")
            
        self.target_file = target_file
