## FiraFiles is a small project to manage files...

#### Created strictly for Windows.

![](https://i.imgur.com/CiVZuym.png)

# Introduction.

**<u>TIP: Run Fira as administrator to get more abelites!</u>**

### Files tree.

![](https://i.imgur.com/B2Smdm7.png)

As you can see on the image, on the top, in <> brackets is located your current work path.

Lower, in [] brackets, typed are folders. (You will use [folder_name] for all time in Fira. Don't forget it.)

After "⋮", without any brackets listed are files.

### Banner.

![](https://i.imgur.com/CiVZuym.png)

Banner is text that shows Fira's logo and title. Inside logo (fire) you can see program version. On the right author nickname is typed.

### Bottom toolbar.

![](https://i.imgur.com/tPyVnRa.png)

On the bottom, you can see white bar. It's called bottom toolbar.

First thing on the bar is your current work location (same as on top).

Next are: selected file and selected dir. You will learn about them later.

### Validators.

![](https://i.imgur.com/SLJPeIO.png)

When you are typing an command, you will see red box on top of the toolbar. It is validator. It shows what is wrong with your input.

### Files commands.

**<mark>All files commands starts with ":".</mark>**

**<>** - Required parameter.

**[]** - Choice parameter. (Use on of possible options.)

| *Command* | *Explanation* | *Requirements* |
| --- | --- | --- |
| `..` | Go to previous directory. |     |
| `cd <dir>` | Go to <dir> directory. |     |
| `sel <file>` | Select <file>. |     |
| `unsel` | Unselect file. | Selected file |
| `dsel <dir>` | Select directory <dir>. |     |
| `dunsel` | Unselect dir. | Selected dir |
| `disk <disk>` | Change work disk. |     |
| `movf` | Move selected file to selected dir. | Selected: dir, file |
| `copyf` | Copy selected file to selected dir. | Selected: dir, file |
| `movd` | Move selected dir to <u>current location</u>. | Selected dir |
| `copyd` | Copy selected dir to <u>current location</u>. | Selected dir |
| `help` | Show help page in command line. |     |
| `refr` | Refresh file tree. |     |
| `find` | Open menu to find an file. |     |
| `cleardisk` | Open menu to clear disks from temp files. |     |
| `:open` | Write selected file content. | Selected file |
|     |     |     |

###

### System commands.

**<mark>All system commands starts with "::".</mark>**

**<>** - Required parameter.

**[]** - Choice parameter. (Use on of possible options.)

| *Command* | *Explanation* |
| --- | --- |
| `checkexist` | Check if config and logs file exists. And repair some basic problems. |
| `cfg [check]` | Deeper check config file and repair more advanced problems. |
| `cfg [refresh]` | Refresh configuration by rereading file and applying config again. |
| `cfg [show]` | Display current configuration. |
| `cfg [set] <entryName> <newValue>` | Change setting. <u>Use "0"-Off / "1"-On as <newValue> parameter</u>. |
| `logs [clear]` | Clear logs file. |
| `logs [show]` | Display logs. |
| `ver` | Display program version. |
| `update [check]` | Check for possible updates. |
| `update [make]` | Make update if there is newer version. |

###

### Configuration.

Configuration file location: `C:\Users\[username]\AppData\Local\.fira\config.ini` or `%USERPROFILE%\AppData\Local\.fira\config.ini`

Available settings, that you can change using `::cfg set` command. (Use those names as <entryName> parameter.)

- `show_banner`
  
- `auto_completion`
  
- `auto_update`
  
- `save_selected_file`
  
- `save_selected_dir`
  
- `save_current_path`
  

Saving `selected_file`/`selected_dir`/`current_path` means automatically saving those things into file. (Config file.) If you exit program, and you have turned on those settings, Fira will open where you ended last session with same saved dir and file, in the same location.

### Logs.

Logs file location: `C:\Users\[username]\AppData\Local\.fira\logs.log` or `%USERPROFILE%\AppData\Local\.fira\logs.log`

Logs are written into file on program main steps informing what happened or didn't. What caused an error etc.

**Log syntax**: `[ date - time ] [ type ] ~ content`

`date` and `time` are automatically generated and putted into log, rest like `type` and `content` are context-based.

`type`: Means which type of log it is. Possible types: `Error`, `Warn`, `Info` and `Startup`.

`content`: It is log content informing what happened.

All process that are logged starts with `- PROCESS_NAME process started -` and ends with `- PROCESS_NAME ended with: [True/False] -`. What does `[True/False]` means? It says if an problem occurred. `True` means, that something unwanted happened, `False` - everything went well.

Some logs are branched into other ones by `|`.

### Find file menu.

![](https://i.imgur.com/AT4Dmpu.png)

This menu contains two inputs: `target` and `location`.

`target`: File that you want to be found. (Type exactly name with extension)

`location`: You can point an location where you want to find file. <u>If you don't know where file is, leave it blank.</u> Program will search every location.

<mark>You can stop process using input by typing `:back`!</mark>

Program will search all files with `target` name. It means, process will

not stop, when founds one file.

### Clear disk menu.

At first, this menu looks weird, but chill, it's easy.

Under `Select which disks you want to be cleaned`, you have listed all of your disks. Under list there's input whose prompt says disk letter. This is basic selection. Choose if you want this disk to be cleaned by typing:

`v`/`yes`/`y`/`1` if you want to select this disk or `x`/`no`/`n`/`0` if you don't.

<mark>You can stop process using input by typing `:back`!</mark>

(This function isn't really good and works best on system disk `C:`)

### Updates.

Fira have implemented automatic updates detector, that after every start checks newest version. If there's newer version than your's local version and <auto_update> setting is on, than update will be automatically installed. If <auto_update> is off, user will be just informed. You can check possible updates by `::update check` and install by `::update make`.
