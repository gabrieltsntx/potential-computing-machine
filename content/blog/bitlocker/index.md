# Bitlocker Powershell and You

[< Back Home](/)

## What is Bitlocker

**Bitlocker** is a Windows security feature that encrypts entire volumes. From a security stand point, this prevent someone from taking a drive from one computer, adding it to another and then reading its contents. 
For maximum security, a **TPM** chip will need to be installed on the computer and enabled.

## The Code!!!

```

#Variables for the drive, encryption status and TPM status
$BitLockerReadyDrive = Get-BitLockerVolume -MountPoint $env:SystemDrive -ErrorAction SilentlyContinue
$encrypt = Get-BitlockerVolume
$tpm = Get-TPM

if($tpm.TpmPresent -eq "True" -and $encrypt.ProtectionStatus -eq "Off")
{
 #Creating the recovery key
 Start-Process 'manage-bde.exe' -ArgumentList " -protectors -add $env:SystemDrive -recoverypassword" -Verb runas -Wait

 #Adding TPM key
 Start-Process 'manage-bde.exe' -ArgumentList " -protectors -add $env:SystemDrive  -tpm" -Verb runas -Wait
 Start-Sleep -Seconds 15 #This is to give sufficient time for the protectors to fully take effect.
 
 #Getting Recovery Key GUID
 $RecoveryKeyGUID = (Get-BitLockerVolume -MountPoint $env:SystemDrive).keyprotector | Where-Object {$_.Keyprotectortype -eq 'RecoveryPassword'} |  Select-Object -ExpandProperty KeyProtectorID

 #Sends Bitlocker key to AD
 Backup-BitLockerKeyProtector -MountPoint $env:SystemDrive -KeyProtectorId $RecoveryKeyGUID

 #Enabling Encryption
 Start-Process 'manage-bde.exe' -ArgumentList " -on $env:SystemDrive -em aes256 -skiphardwaretest -usedspaceonly" -Verb runas -Wait
}

```
