from django.core.management.base import BaseCommand

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = "Scans through the given app for faulty imports, or the entire project directory if no apps are specified"
    args = '[appname ...]'
    requires_model_validation = False

    def import_statement_extractor(self, directory_path, python_file):
        python_file = '%s/%s' % (directory_path, python_file)
        file_content = open(python_file).readlines()
        line_number = 0
        for line in file_content:
            line_number += 1
            line = line.strip()
            if not line.startswith('#') or not line.startswith("'''"):
                if line.startswith('from ') or line.startswith('import '):
                    try:
                        exec(line)
                    except ImportError, e:
                        print '%s(line:%s) Reason:%s' % (python_file, line_number, e.__str__())
                    except Exception, e:
                        print '%s(line:%s) Reason:%s' % (python_file, line_number, e.__str__())

    def directory_py_files(self, parent_directory):
        import os
        directory_generator = os.walk(parent_directory)
        directory_info = directory_generator.next()
        for file_name in directory_info[2]:
            if file_name.endswith('py'):
                self.import_statement_extractor(directory_info[0], file_name)
        for directory in directory_info[1]:
            if not directory.startswith('.'):
                self.directory_py_files('%s/%s' % (parent_directory, directory))

    def handle(self, *app_labels, **options):
        from django.conf import settings
        import sys
        if hasattr(settings, 'ROOT_PATH'):
            ROOT_PATH = settings.ROOT_PATH
        else:
            import os
            ROOT_PATH = os.getcwd()
        if not app_labels:
            self.directory_py_files(ROOT_PATH)
            sys.exit()
        for app_label in app_labels:
            if app_label not in settings.INSTALLED_APPS:
                sys.exit("Supplied app '%s' is not part of this project. Please mention a proper app name" % app_label)
        for app_label in app_labels:
            self.directory_py_files(settings.ROOT_PATH + "/" + app_label)
