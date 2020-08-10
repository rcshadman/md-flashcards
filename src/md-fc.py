#! /d/Code/md-flashcards/env/Scripts/python
import os
import sys
import re
import fire
from pprint import pprint
from PyInquirer import prompt
from pyfiglet import Figlet


class COLORS:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class App:
    """
    Markdown to Flashcards searches the given file(s) for flashcards and converts them to flashcards that can be imported into anki

    Flashcard Markdown Syntax:
    !--!
    front
    ++
    back
    ++
    other
    ++
    !--!

    Commands:
        create <markdownfile> <outputfile> - Uses the inputfile parses (the above described) syntax and exports it as a csv.

    """

    def __init__(self):
        # Keep track of all the cards
        self.__cards = []
        # The input file
        self.__in_file = ''
        # The output file
        self.__out_file = ''
        # Keep track of all the contents of the file
        self.__file_content = ''
        # vebose mode ()
        self.verbose = 'false'
        self.seperator = ';'

    def __print_error(self, text):
        print(f"{COLORS.RED}{text}{COLORS.RESET}")

    def __print_warning(self, text):
        print(
            f"{COLORS.YELLOW}[WARNING]: {text}{COLORS.RESET}")

    def __print_success(self, text):
        print(f"{COLORS.GREEN}{text}{COLORS.RESET}")

    def __print_verbose(self, text):
        if self.verbose != 'false':
            print(
                f"{COLORS.CYAN}[INFO]: {text}{COLORS.RESET}")

    def __save_cards(self):
        """Saves the cards in the given file path using the seperator to separate the fields   """
        line_count = 0
        # Open the file
        with open(self.__out_file, 'w') as outFile:
            self.__print_verbose(f"Opening: {self.__out_file}")
            # Write all the cards
            for card in self.__cards:
                try:
                    to_write = f"{card['front']}{self.seperator}{card['back']}{self.seperator}{card['other']}\n"
                    outFile.write(to_write)
                    line_count += 1

                    self.__print_verbose(
                        f"Writing card #{line_count}: {card['front']};{card['back']};{card['other']}")

                except Exception as e:
                    self.__print_verbose(
                        f"An error occurred: {e}")
                    # NOT INCREMENTING LINE COUNT, so we can still check if something went wrong even if we are not in verbosemode

        # If the line_count is not equal to the length of the cards something went wront.
        if not line_count == len(self.__cards):
            self.__print_warning("Could not write all flashcards...")

        self.__print_success(
            f"Wrote {line_count} flashcards to: {self.__out_file}. The fields are `{self.seperator}` sepperated.")

    def __check_files(self) -> bool:
        """Checks the given input and output files

        Returns:
            bool: Returns True if everything is okay, otherwise returns False.
        """
        # Check if the input file exists
        if not os.path.exists(self.__in_file):
            self.__print_error(
                f"{self.in_file} does not exist, please choose an existing file.")
            return False
        # Check if the output path still is available
        if os.path.exists(self.__out_file):
            print(COLORS.GREEN)
            overwrite = prompt(
                [{"type": "confirm", "message": f"{self.__out_file} already exists, do you want to overide?", 'name': "overide", 'default': False}])
            print(COLORS.RESET)
            if not overwrite['overide']:
                return False

        return True

    def __parse_cards(self):
        """Parses the cards and saves all the card info in self.cards """
        tags = self.content.split("!--!")
        if len(tags) < 1:
            self.__print_error(
                "No flashcards could be found, please check if you used the correct syntax and saved the file!")
            sys.exit(1)

        flash_cards_contents = []
        for i, tag in enumerate(tags):
            # Check if the card is not even (this filters out the space between two different tags & the start of the document)
            if i % 2 != 0:
                flash_cards_contents.append(tag)

        self.__print_verbose(
            f"Found: {len(flash_cards_contents)} possible cards")

        if len(flash_cards_contents) < 1:
            self.__print_error(
                "No flashcards could be found, please check if you used the correct syntax and saved the file!")
            sys.exit(1)

        for i, flash_card in enumerate(flash_cards_contents):
            data = flash_card.split("++")
            if len(data) < 3:
                self.__print_error(
                    f"Not enough fields were given in card #{i+1}")
                sys.exit(1)
            front, back, other = data
            self.__cards.append(
                {"front": front.strip(), "back": back.strip(), "other": other.strip()})

        self.__print_verbose(f"Found {len(self.__cards)} flashcards!")

    def create(self, inputfile, outputfile):
        """Create the flashcards from <inputfile> and save them to <outputfile>

        Args:
            inputfile (str): The filename of the file the flashcards need to be extracted from
            outputfile (str): The filename of the file the flashcards should be saved to.
        """
        self.__in_file = inputfile
        self.__out_file = outputfile
        if not self.__check_files():
            sys.exit(1)
        with open(inputfile, 'r') as f:
            self.content = f.read()

        if len(self.content) < 1:
            self.__print_error('This file does not contain anything!')
            sys.exit()

        self.__parse_cards()
        self.__save_cards()


if __name__ == "__main__":
    os.system("")  # Make colors work :)
    fire.Fire(App)
    banner = Figlet(font='slant')
    print(COLORS.CYAN)
    print(banner.renderText('Markdown'))
    print(banner.renderText(' > > > > > '))
    print(banner.renderText('Flashcards'))
    print(COLORS.RESET)
