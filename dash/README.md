# Dash Console.
~ Small project to make terminal usage easier. Work's only on Windows.


## Author

- [@gental-py](https://www.github.com/gental-py)


## Features
- Easy to use.
- Full customization.
- Custom commands.
- Custom separator.
- Easy and clear interface.
- Lot of commands


## Files localization:
#### `Main folder` - `C:\Users\USERNAME\Appdata\Local\.dash\`
#### `Users` - `C:\Users\USERNAME\Appdata\Local\.dash\users\`
#### `Backup` - `C:\Users\USERNAME\Appdata\LocalLow\.dash_recovery\`
#### `Modules` - `C:\Users\USERNAME\Appdata\Local\.dash\online\`


## What is `sepchar`?
Sepchar is character that will separate arguments. Deafult = `,`. Example: `var.add , Age , 21` 


## Commands
| Command                        | Effect                                     |
|--------------------------------|--------------------------------------------|
|     **Basics**                 |                                            |
| `exit`                         | Exit program.                              |
| `restart`                      | Restart program.                           |
| `cls`                          | Clear screen.                              |
|     **Config**                 |                                            |
| `mycfg`                        | Display current config.                    |
| `set.cursor <cursor>`          | Set new cursor.                            |
| `set.sepchar <sepchar>`        | Set new sepchar.                           |
| `set.oschar <oschar>`          | Set new system command prefix.             |
|     **Network**                |                                            |
| `netinfo`                      | Display your network info.                 |
| `dnslkp <target.addr>`         | Dns lookup an addres.                      |
| `revdnslkp <target.ip>`        | Reversed DNS lookup. (ip->addr)            |
| `ipgeoinfo <target.ip>`        | Returns ip geo location. (Country, city)   |
| `req.get <response> <url>`     | Make request and return [code/text]        |
|     **Dash Registry**          |                                            |
| `dreg.show`                    | Show entries and values.                   |
| `dreg.edit <entry> <value>`    | Change entry value. [true/false]           |
| `dreg.copy`                    | Copy current registry code.                |
| `dreg.paste <code>`            | Paste registry code.                       |
| `dreg.reset`                   | Reset registry.                            |
|     **Custom Commands**        |                                            |
| `<custom.name>`                | Execute custom command.                    |
| `cstm.add <name>`              | Create custom command.                     |
| `cstm.open`                    | Open custom commands file.                 |
| `cstm.convert <mode> <%path>`  | Convert py script to dash. <text/file>     |
| `cstm.list`                    | Lists all custom commands.                 |
|     **Variables**              |                                            |
| `var.list`                     | Lists all variables and their values.      |
| `var.add <name> <value>`       | Create variable and assign value.          |
| `var.rem <name>`               | Remove variable.                           |
| `var.set <name> <value>`       | Assign new value for variable.             |
|     **Recovery**               |                                            |
| `rcv.save`                     | Save current user files image.             |
| `rcv.restore`                  | Restore saved files.                       |
|     **Accounts (as root)**     |                                            |
| `acc.create <name> <pass>`     | Create account.                            |
| `acc.delete <name>`            | Delete account.                            |
| `acc.chngpasswd <name> <pass>` | Change an account password.                |
| `acc.logout`                   | Brings you back to login screen.           |
| `acc.rename <name> <newname>`  | Rename an account.                         |
| `acc.chngmode <name> <mode>`   | Change an account mode. <root/user>        |
| `acc.list`                     | Shows list of all accounts.                |
|     **Accounts (as user)**     |                                            |
| `acc.chngpasswd <pass> <new>`  | Change current account password.           |
| `acc.logout`                   | Brings you back to login screen.           |
| `acc.rename <newname>`         | Change current account name.               |
| `acc.list`                     | Show list of all accounts.                 |
|     **Packages**               |                                            |
| `dget.info <name>`             | Returns informations abaout package.       |
| `dget.onlinelist`              | Returns all available packages.            |
| `dget.list`                    | Show all installed packages.               |
| `dget.get <name>`              | Install package.                           |
| `dget.remove <name>`           | Remove package.                            |
|     **Other**                  |                                            |
| `viewf <path>`                 | Display file with simple highlithing.      |
| `checkver`                     | Shows local version and check for updates. |
| `checkfiles`                   | Check program files health.                |
| `debg.exe <command>`           | Execute command.                           |


## Registry (dreg)
| Index | Entry                          | Effect                                          | Deafult |
|-------|--------------------------------|-------------------------------------------------|---------|
|   1   | `loginNameAsNumber`            | Shows names and their index and ask for index.  |    F    |
|   2   | `checkArgLenght`               | Checks arguments lenght.                        |    T    |
|   3   | `spaceAfterCursor`             | Add's space after cursor. T/F: (> text) (>text) |    T    |
|   4   | `enableColors`                 | Turn on colors. (Recomended for easier usage)   |    T    |
|   5   | `copyOutput`                   | Automaticly copying some commands output.       |    F    |
|   6   | `showBootupInfo`               | Requires to press any key after read boot logs. |    F    |
|   7   | `enableCustomCommands`         | Enables custom commands.                        |    T    |
|   8   | `advancedErrorOutput`          | Show more informations about errors. (Advanced) |    F    |
|   9   | `autoUpdate`                   | Automaticly install updates when detected.      |    F    |


## Accounts
Every account have own: custom commands, custom variables, config and `account` file.

Account can have: `root` or `user` permissions.
`Root`:
Can do everything excepting editing `[root]` account. (Deafult account) 

`User`:
Have limited permissions. Cannot edit dregistry, manage other account. (Can change name and password for their own)
Can manage their config and custom files.

Passwords security:
All passwords are encrypted and hashed using `bcrypt` module. Password cannot be decoded to string, but can be brute-forced.


## Custom commands
Custom commands are commands made by users. You can also create your own in python3. 

### Tutorial:
Let's create command, that will be generate random number.

Step 1. - Create python code.
```python
# Command syntax:  random, <min>, <max>
import random as r

min = __Command__[1]  # first argument given in input
max = __Command__[2]  # and second one.

number = r.randint(min,max)
print(f"  Your number is: {number}")
```

Step 2. - Convert command.
1. Copy python file localization.
2. In Dash, type command: `cstm.convert, file, <%path>`
3. Command will output one-line code. (Copy command)

Step 3. - Create custom command.
1. Enter command: `cstm.add, random` (random is <name>)
2. Than notepad will apear. Find `[random]` and change `value` to your code.
  
Step 4. - End process.
1. You can close notepad now.
2. Enter command name and arguments to execute command.
  
`random, 1, 10` - outputs random number between 1 and 10.


## dget - Custom package manager.
Packages are located in this github repo, in <online> folder. If you want to public your custom module, request me to do that.



