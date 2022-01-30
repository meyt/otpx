# otpx

Simple OTP Client

Supported algorithms:
[TOTP](https://tools.ietf.org/html/rfc6238)
and [HOTP](https://tools.ietf.org/html/rfc4226)

> Important note: Secrets must be stored in plain-text.

## Requirements

- Python >= 3.5


## Install


```
pip install otpx
```

## Usage

Create keys file like this in home path `~/.otpx/keys`:

```
instagram1: JBSWY3DPEHPK3PXP
instagram2: 3DPEHP3PXPJBSWYK
github: DPEHPKY3PXP3JBSW
myhotp: KJBSWDY3PXP3PEHP 1
```

Get all codes:

```
otpx
```

Get one code:

```
otpx instagram1
```

Copy to clipboard:

```
otp copy instagram2
```

Increase HOTP counter and get the code

```
otp inc myhotp
```


## `keys` file format

```
# comment
name: secret [HOTP counter]
```
