from src import model
import src.uml_output as uml_out


class Controller:
    def __init__(self, command_reader, argument_reader):
        # Command line argument variables
        self.command_reader = command_reader
        self.arguement_reader = argument_reader
        self.files = None
        self.statistics = None
        self.output_location = None
        self.extracted_modules = None

    def run_console(self):
        self.command_reader.cmdloop('Starting prompt...\n'
                                    'Type "help" for commands')

    # Edited by Jake
    @staticmethod
    def run_parser(self, hide_attributes, hide_methods):
        if len(self.controller.files) > 0:
            # Initiate processor
            processor = model.FileProcessor(self.controller.statistics)
            processor.process_files(self.controller.files)

            self.controller.extracted_modules = processor.get_modules()

            new_uml = uml_out.MakeUML(hide_attributes, hide_methods)
            return new_uml.create_class_diagram(self.controller.extracted_modules)
        else:
            print("Error: No files were set, use command change_python_files")