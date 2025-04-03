# Bitlocker Powershell and You

[< Back Home](/)

## What is Bitlocker

**Bitlocker** is a Windows security feature that encrypts entire volumes. From a security stand point, this prevent someone from taking a drive from one computer, adding it to another and then reading its contents. 
For maximum security, a **TPM** chip will need to be installed on the computer and enabled.

## The Code!!!

```
$BitLockerReadyDrive = Get-BitLockerVolume -MountPoint $env:SystemDrive -ErrorAction SilentlyContinue
$encrypt = Get-BitlockerVolume
$tpm = Get-TPM
if($tpm.TpmPresent -eq "True" -and $encrypt.ProtectionStatus -eq "Off")
{
 Start-Process 'manage-bde.exe' -ArgumentList " -protectors -add $env:SystemDrive -recoverypassword" -Verb runas -Wait
 Start-Process 'manage-bde.exe' -ArgumentList " -protectors -add $env:SystemDrive  -tpm" -Verb runas -Wait
 Start-Sleep -Seconds 15
 $RecoveryKeyGUID = (Get-BitLockerVolume -MountPoint $env:SystemDrive).keyprotector | Where-Object {$_.Keyprotectortype -eq 'RecoveryPassword'} |  Select-Object -ExpandProperty KeyProtectorID
 Backup-BitLockerKeyProtector -MountPoint $env:SystemDrive -KeyProtectorId $RecoveryKeyGUID
 Start-Process 'manage-bde.exe' -ArgumentList " -on $env:SystemDrive -em aes256 -skiphardwaretest -usedspaceonly" -Verb runas -Wait
}
```

## Breaking it down

```
$BitLockerReadyDrive = Get-BitLockerVolume -MountPoint $env:SystemDrive -ErrorAction SilentlyContinue
$encrypt = Get-BitlockerVolume
$tpm = Get-TPM
```

The first portion checks and gets the system drive, typically C:. It also gets the details for the TPM.
Depending on the status of the TPM, it will proceed in the next part. It checks to make sure that a TPM chip is present and that the drive isn't already encrypted.

```
if($tpm.TpmPresent -eq "True" -and $encrypt.ProtectionStatus -eq "Off")
```

If it passes that quick check, the script with then proceed to add protects. One is the recovery key that is really long and the other is the TPM chip.
After running the commands for adding the protectors, it waits a few moments to make ensure that the computer has finished created them.

```
Start-Process 'manage-bde.exe' -ArgumentList " -protectors -add $env:SystemDrive -recoverypassword" -Verb runas -Wait
Start-Process 'manage-bde.exe' -ArgumentList " -protectors -add $env:SystemDrive  -tpm" -Verb runas -Wait
Start-Sleep -Seconds 15
```

The next step is to get the recovery key information and send it over to the computers DC for storage in the computers object properties in the companies AD.
This can be modified to instead send the information to Entra ID if the computer is cloud joined only.
That can be done using **BackupToAAD-BitLockerKeyProtector** instead of **Backup-BitLockerKeyProtector**

```
$RecoveryKeyGUID = (Get-BitLockerVolume -MountPoint $env:SystemDrive).keyprotector | Where-Object {$_.Keyprotectortype -eq 'RecoveryPassword'} |  Select-Object -ExpandProperty KeyProtectorID
Backup-BitLockerKeyProtector -MountPoint $env:SystemDrive -KeyProtectorId $RecoveryKeyGUID
```

Finally, the last part actually starts the process of encrypting the drive. 
The **-skiphardwaretest** argument permits the bitlocker encryption process to start and complete without having to reboot the computer.
The **-usedspaceonly** speeds up the encryption process by encrypting the part of the drive that currently has data.

```
Start-Process 'manage-bde.exe' -ArgumentList " -on $env:SystemDrive -em aes256 -skiphardwaretest -usedspaceonly" -Verb runas -Wait
```