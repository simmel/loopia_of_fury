# loopia\_of\_fury

A "DynDNS" client for Loopia when you have MFA/BankID enabled

## Installation

### Standalone usage
```terminal
# You should specify a version with ==1.a.released.version
$ pip3 install loopia_of_fury
```

### Container usage
```terminal
# You should specify a version with :1.a.released.version
$ docker run darksoy/loopia_of_fury
```

## Usage

By default `loopia_of_fury` uses https://dyndns.loopia.se/checkip to determine
your external IP.
```terminal
$ loopia_of_fury --user youruser@loopiaapi --password supersecretpassword
$ # or
$  export LOOPIA_PASSWORD=supersecretpassword
$ loopia_of_fury --user youruser@loopiaapi
```

### Specify which IP to use

```terminal
$ loopia_of_fury --user youruser@loopiaapi --ip 192.0.2.1
```
