# Finding Something

## in a File System

### using PowerShell

#### and stuff

[< Back](/Notes)

### The code!!!

```
Get-ChildItem -Recurse -Path "C:\" -ErrorAction SilentlyContinue | Where-Object {$_.Name -like "*fileName*"}
```

### Breaking it down

Get-ChildItem lists items (files, folders) in a directory.
The -Recurse flag states that it should also look in directory within the specified directory all the way down.
-Path is the start point and -ErrorAction is to handle directories that you do not have access to. Without the SilentlyContinue parameter specified, the output would be filled with red text.

Following the bar, we specify what we are looking for. It states if an object has a property of Name that is like *fileName* then return it. 







