# UniWorX Monitor

Automatable Python script to monitor LMU UniWorX courses.

> IF YOU HAVE ANY PROBLEM AND IMPROVEMENT IDEA, PLEASE [OPEN AN ISSUE](https://github.com/changkun/UniWorXMonitor/issues)  OR START A PULL REQUEST THAT HELPS ME IMPROVE THIS PROJECT.

## Usage

### **Basics**:

- [x] **Make sure** that you have [Python](https://www.python.org/) and [Pip](https://pypi.python.org/pypi/pip) running on your OS;
- [x] Clone this repo to your local folder;
- [x] `cd` into that folder for further operations. 

### **Install dependencies**:

```bash
sudo pip install -r requirements.txt
# or
sudo pip3 install -r requirements.txt
```

### **Configure your account**:

Fill your information inside [infos.json](./infos.json)

### **Run**:

```bash
python main.py
# or
python3 main.py
```

> **Note**:
> 
> 1. Your first execution will create a json file to store all courses status if you removed the courses.json inside the repo folder;
> 2. **Afterwards** every time you execute this script can monitor the UniWorX for any course status change;
> 3. Terminal output gives you the up-to-date changes informations for you, you can also check the `log.txt` for change history.

## Example Result

**Local store sample**:

[courses.json](./courses.json)

**Local logs**:

[log.txt](./log.txt)

**Execution sample**:

![](./example.png)

## AUTOMATED TASK

### for macOS

Every day automated execution with notification. 

**Example:**

![](autotask/noti.png)

Please read [autotask/README.md](autotask/README.md) for setup guide.

### for Windows/Linux

You might need find your own setup method, but PR welcome!

## License

[MIT](./LICENSE)
