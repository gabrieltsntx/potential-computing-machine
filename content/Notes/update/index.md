# Windows Updates

This is specifically to run windows updates from the terminal.

## Using PowerShell

There are a few steps to take in order to run updates from the terminal.

- Set Execution Policy to Bypass
- Install Module PSWindowsUpdate
- Run PSWindowsUpdate
- Schedule Reboot if needed
- Troubleshoot as needed

### Execution Policy

The execution policy is a __security feature__ that is meant to stop threat actors from running malicious scripts.
We are going to need to bypass the default policy, **Restricted** in order work on the computer.

You can check the current policy by:

```
Get-ExecutionPolicy
```

We are going to change it by:

```
Set-ExecutionPolicy Bypass
```

### Install Module PSWindowsUpdate

Run the following to start the install process. If this is your first time running an install command on a computer, you may be prompted to update NuGet and whether you trust the PSGallery. Type Y for both and press enter.

```
Install-Module -Name PSWindowsUpdate
```

### Run PSWindows Update

This is where we may start to encounter some issues that will require some troubleshooting.

To start run:

```
Get-WindowsUpdate -AcceptAll -Install
```

The line above will get all pending available updates, accept the download and start the install process.
You can also add the -AutoReboot flag if you know the computer is not being worked on.
If all goes well, that is pretty much the end of it. Just schedule a reboot if needed.

### Schedule Reboot

This can be handled a couple of ways but the easisest is from our scipts in ConnectWise.
Right click the computer in question, navigate to Scripts > Actions > *Schedule Reboot.
That will schedule a reboot to run at midnight and you can view it from Task Scheduler on the computer.

### Troubleshooting

There are a lot of things that could go wrong but here are some of the more general steps that you can take that have worked for me.

If you've entered the PSWindowsUpdate command but nothing is happening, first try pressing Enter. If nothing changes, we're going to have to open the Windows Update Troubleshooter.

From the terminal run:
```
msdt.exe /id WindowsUpdateDiagnostic
```

This will open up a new window. From there run the troubleshooter and try again.

Some error logs that have helped in the past are located in C:\Windows\Panther.
Also looking up the KB number for a patch that fails to install has proved useful in the past.
