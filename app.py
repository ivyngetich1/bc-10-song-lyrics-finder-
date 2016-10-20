"""
Usage:
    my_program findsong <song_name>
    my_program viewsong <song_id>
    my_program savesong <song_id>
    my_program songclear <song_clear>
    my_program (-i | --interactive)
    my_program (-h | --help | --version)

Arguments:
    song_id     Use findsong command to view song ID
    song_id     Input song_id to viewsong command  to view the lyrics of the song 
    song_id    Input song_id to savesong command to save song locally
    songclear   Input any character to  songclear command to prompt for delete or exit of  the local database
"""

import sys
import os
import cmd
from docopt import docopt, DocoptExit
from mylyrics import songfind, songview, savesong,songclear
from pyfiglet import figlet_format 
from termcolor import colored, cprint


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

def intro():
    os.system("clear")
    cprint(figlet_format('WELCOME TO LOCK IN THE LYRICS', font='digital'),'green', attrs=['bold', 'blink'])
    print(colored(__doc__))


class MyInteractive (cmd.Cmd):
    prompt = '<lyrics>>>'
    file = None

    @docopt_cmd
    def do_findsong(self, arg):
        """Usage: findsong <song_name>"""
        songfind(arg['<song_name>'])

    @docopt_cmd
    def do_viewsong(self, arg):
        """Usage: viewsong <song_id>"""
        songview(arg['<song_id>'])

    @docopt_cmd
    def do_savesong(self, arg):
        """Usage: savesong <song_id>"""
        savesong(arg['<song_id>'])
        
    @docopt_cmd
    def do_songclear(self, arg):
        """Usage: songclear <song_clear>"""
        songclear(arg['<song_clear>'])
        
    

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    os.system("clear")
    intro()
    MyInteractive().cmdloop()

print(opt)
