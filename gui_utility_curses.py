import curses
import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.stdout.decode('utf-8'), e.stderr.decode('utf-8')

def display_output(stdscr, output, error):
    stdscr.clear()
    output_lines = output.splitlines()
    error_lines = error.splitlines()
    max_y, max_x = stdscr.getmaxyx()
    current_line = 0

    while True:
        stdscr.clear()
        for i, line in enumerate(output_lines[current_line:current_line + max_y - 2]):
            stdscr.addstr(i, 0, line[:max_x-1])

        if error_lines:
            stdscr.addstr(max_y-2, 0, "Error:")
            stdscr.addstr(max_y-1, 0, error_lines[0][:max_x-1])
        
        stdscr.addstr(max_y-1, 0, "Press 'q' to go back, 'j' to scroll down, 'k' to scroll up")

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('j') and current_line + max_y - 2 < len(output_lines):
            current_line += 1
        elif key == ord('k') and current_line > 0:
            current_line -= 1

    stdscr.clear()
    stdscr.refresh()

def get_user_input(stdscr, prompt):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    user_input = stdscr.getstr().decode('utf-8')
    stdscr.refresh()
    curses.noecho()
    return user_input

def execute_and_display(stdscr, command):
    output, error = run_command(command)
    display_output(stdscr, output, error)

def main_menu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Highlighted text
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Normal text

    menu = [
        "Add User",
        "Modify User",
        "Delete User",
        "List Users",
        "Add Group",
        "Modify Group",
        "Delete Group",
        "List Groups",
        "Disable User",
        "Enable User",
        "Change Password",
        "About",
        "Exit"
    ]
    descriptions = [
        "Add a user to the system.",
        "Modify an existing user.",
        "Delete an existing user.",
        "List all users on the system.",
        "Add a user group to the system.",
        "Modify a group and its list of members.",
        "Delete an existing group.",
        "List all groups on the system.",
        "Lock the user account.",
        "Unlock the user account.",
        "Change Password of a user.",
        "Information about this program.",
        "Exit the program."
    ]

    current_row = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        for idx, row in enumerate(menu):
            x = width // 2 - len(row) // 2
            y = height // 2 - len(menu) // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(2))

        description_x = width // 2 - len(descriptions[current_row]) // 2
        description_y = height // 2 + len(menu) // 2 + 1
        stdscr.addstr(description_y, description_x, descriptions[current_row])

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:

            if current_row == 0:
                username = get_user_input(stdscr, "Enter username: ")
                execute_and_display(stdscr, f"sudo useradd {username}")
            elif current_row == 1:
                username = get_user_input(stdscr, "Enter username: ")
                new_username = get_user_input(stdscr, "Enter the new username: ")
                execute_and_display(stdscr, f"sudo usermod -l {new_username} {username}")
            elif current_row == 2:
                username = get_user_input(stdscr, "Enter username: ")
                execute_and_display(stdscr, f"sudo userdel -r {username}")
            elif current_row == 3:
                execute_and_display(stdscr, "cut -d: -f1 /etc/passwd")
            elif current_row == 4:
                groupname = get_user_input(stdscr, "Enter group name: ")
                execute_and_display(stdscr, f"sudo groupadd {groupname}")
            elif current_row == 5:
                groupname = get_user_input(stdscr, "Enter group name: ")
                new_groupname = get_user_input(stdscr, "Enter the new group name: ")
                execute_and_display(stdscr, f"sudo groupmod -n {new_groupname}{groupname}")
            elif current_row == 6:
                groupname = get_user_input(stdscr, "Enter group name: ")
                execute_and_display(stdscr, f"sudo groupdel {groupname}")
            elif current_row == 7:
                execute_and_display(stdscr, "cut -d: -f1 /etc/group")
            elif current_row == 8:
                username = get_user_input(stdscr, "Enter username: ")
                execute_and_display(stdscr, f"sudo usermod --lock {username}")
            elif current_row == 9:
                username = get_user_input(stdscr, "Enter username: ")
                execute_and_display(stdscr, f"sudo usermod --unlock {username}")
            elif current_row == 10:
                username = get_user_input(stdscr, "Enter username: ")
                execute_and_display(stdscr, f"sudo passwd {username}")
            elif current_row == 11:
                stdscr.addstr(0, 0, "This is a simple user management program built with curses.")
                stdscr.refresh()
                stdscr.getch()
            elif current_row == 12:
                break

        stdscr.refresh()

curses.wrapper(main_menu)
