User and Group Management Utility with Curses

This Python program provides a command-line interface using the "curses" library to manage users and groups on a Linux system. The utility allows administrators to add, modify, delete, list users and groups, and manage user accounts through an interactive menu.

You can perform the following actions:
1. Add User
2. Modify User
3. Delete User
4. List Users
5. Add Group
6. Modify Group
7. Delete Group
8. List Groups
9. Disable User
10. Enable User
11. Change Password

Run the program: Execute the Python script.
python3 gui_utility_curses.py

Navigate the menu:

Use the UP and DOWN arrow keys to move between menu options.
Press ENTER to select an option.
Follow the prompts to enter necessary information (e.g., username or group name).
Press 'q' to go back, 'j' to scroll down, 'k' to scroll up while viewing command output.

Requirements
Linux operating system
Python 3.x
"curses" library (included in the Python standard library)

Notes
This utility requires superuser (root) privileges to manage users and groups. Ensure you have the necessary permissions to execute the commands.
Use this utility with caution, especially when modifying or deleting users and groups, as it can affect system configuration and user data.