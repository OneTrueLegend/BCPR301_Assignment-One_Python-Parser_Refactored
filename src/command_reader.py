from cmd import Cmd
from tkinter import filedialog, Tk
from subprocess import call

from src.csv_plugin import CSV_handler
from src.model import FileProcessor
from src.pickle_modules import PickleModules
from src.python_code_validator import CodeValidator
from src.uml_output import MakeUML
import os


class CommandReader(Cmd):
    def __init__(self, controller):
        Cmd.__init__(self)
        # Command line argument variables
        self.controller = controller
        self.prompt = '> '

    def do_enable_statistics(self, args):
        """
        Enabled statistics collection
        Author: Jake Reddock
        Syntax: enable_statistics
        """
        self.controller.enable_statistics()

    def do_show_statistics(self, args):
        """
        Show statistics about the analysed classes
        Author: Jake Reddock
        Syntax: show_statistics
        Requires: enable_statistics, output_to_dot
        """
        if self.controller.statistics is not None:
            if self.controller.extracted_modules is not None:
                print("Creating graph, please wait...")
                self.controller.statistics.show_graph_data()
            else:
                print("Please run the \"output_to_dot\" to command")
        else:
            print(
                "Statistics collecting is not enabled, type \"enable_statistics\" to enable")

    def do_change_python_files(self, args):
        """
        Change input files that are to be parsed by system
        Author: Braeden
        Syntax: change_python_files <filenames.py>
        """
        user_args = args.split()
        if len(user_args) > 0:
            self.controller.files = [args]
        else:
            print("Syntax Error: change_python_files <filenames.py>")

    # Edited By Jake
    def do_output_to_dot(self, args):
        """
        Parse and output the file into a UML diagram
        Author: Braeden
        Syntax: output_to_dot [-a|-m]
        [-a] Hides all attributes on class diagram
        [-m] Hides all methods on class diagram
        """
        user_options = args.split()

        hide_attributes = False
        hide_methods = False

        if len(user_options) > 0:
            if "-a" in user_options:
                hide_attributes = True
            if "-m" in user_options:
                hide_methods = True

        self.controller.run_parser(self, hide_attributes, hide_methods)

    def do_set_input_file(self, args):
        """
        Sets the input file that will be converted into a UML diagram.
        Author: Jake Reddock
        Syntax: set_input_file [file_name]
        """
        if len(args) == 0:
            root = Tk()
            self.controller.set_input_files(filedialog.askopenfilenames(
                initialdir="C:/",
                title="Select Input File",
                filetypes=(
                    ("Python Files",
                     "*.py"),
                    ("all files",
                     "*.*"))))
            root.withdraw()
        else:
            self.controller.set_input_files([args])

    # Created by Michael Huang
    def do_output_to_file(self, args):
        """
        Sets the output of the class diagram to a file location.
        Author: Michael Huang
        Syntax: output_to_file
                output_to_file [path]
        """

        from shutil import copyfile
        if len(args) == 0:

            root = Tk()
            root.filename = filedialog.askdirectory()
            print(root.filename)
            root.withdraw()

            copyfile('../tmp/class.png', root.filename + '/class.png')
        else:
            try:
                copyfile('../tmp/class.png', args + '/class.png')
                print('The output to the file destination was successful.')
            except FileNotFoundError as f:
                print('Failed to find a file: %s' % f)
                print('Please specify a valid file path.')
            except:
                print('Unexpected error has occurred.')

    @staticmethod
    def do_output_to_png(args):
        """
        Converts dot file into PNG
        Author: Braeden
        """
        # TODO Not working yet as cannot test with Ara computers
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
        return call(['dot', '-Tpng', 'tmp/class.dot', '-o', 'tmp/class.png'])

    def do_validate_py(self, args):
        '''
        Validates a single file as executable python code.
        Author: Peter
        '''
        files = []
        if type(args) == str:
            files.append(args)
        elif type(args) == list:
            files = args

        check_code = CodeValidator()
        validated_file = check_code.validate_files(files)

    def do_save_to_csv(self, params):
        '''
        Saves specified file to csv.
        [command_line] input_file output_file
        Author: Peter
        '''
        # print(params, type(params))
        input_file = []
        if params == '':
            params = 'plants.py output.csv'
        args = params.split(' ')
        # print(args)
        if len(args) >= 1:
            input_file.append(args[0])
            output_file = 'output.csv'
        if len(args) >= 2:
            output_file = args[1]
        if input_file[0].endswith('.py'):
            fileprocessor = FileProcessor()
            fileprocessor.process_files(input_file)
            modules = fileprocessor.get_modules()
            # print(modules)
            csv_writer = CSV_handler()
            if csv_writer.write_csv_file(modules, output_file):
                print('File successfully saved as {}'.format(output_file))

    def do_load_csv_for_uml(self, params):
        '''
        Loads csv file and creates UML diagram
        [command line] [file.csv]
        Author: Peter
        '''
        if params == '':
            params = 'output.csv'
        args = params.split(' ')
        print(args)
        if len(args) >= 1:
            input_file = args[0]
        if input_file.endswith('.csv'):
            csvloader = CSV_handler()
            module = csvloader.open_file(input_file)
            makediagram = MakeUML(True, True)
            if makediagram.create_class_diagram(module):
                print(
                    "{} successfully converted to UML class diagram".format(input_file))

    def do_pickle_modules(self, filename='plants.py'):
        '''
        Load modules from single file and save them using pickle
        Author: Peter

        Command:
        pickle_modules filename
        eg pickle_modules plants.py
        '''
        file = [filename]
        parser = FileProcessor()
        parser.process_files(file)
        modules = parser.get_modules()
        pickler = PickleModules()
        return pickler.save(modules)

    def load_pickle(self):
        '''
        Loads previously saved module using pickle
        Author: Peter

        Command:
        load_pickle
        '''
        pickler = PickleModules()
        return pickler.load()

    def do_quit(self, other):
        '''
        Quits programme.
        Author: Peter
        '''
        print("Goodbye ......")
        return True
