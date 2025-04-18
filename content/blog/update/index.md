# Windows Updates

This is specifically to run windows updates from the background.

## Using PowerShell

There are a few steps to take in order to run updates from the background.

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

