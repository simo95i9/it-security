# Mandatory 1


## The problem

We are given a python script that looks like this

```python
# nslookup-vulnerable.py
import subprocess

def main():
    domain_name = input("Enter the domain name: ")
    command = "nslookup {}".format(domain_name)
    response = subprocess.check_output(command, shell=True, encoding="UTF-8")

    print(response)


if __name__ == '__main__':
    main()

```


The trouble with this script is that it is vulnerable to an injection attack,
so if we were hosting a web service where user input was passed directly to
this script, malicious user could run arbitrary commands on our hardware!


A malicious user input could look like this

```shell
$ python3 nslookup-vulnerable.py
Enter the domain name: kea.dk; ls; echo 'oh no evil happened'
Server:         10.200.10.10
Address:        10.200.10.10#53
Non-authoritative answer:
Name:   kea.dk
Address: 89.34.18.61

cryptographically-secure-randomness.py                                                            
mandatory-1.md
nslookup-invulnerable.py
nslookup-vulnerable.py
oh no evil happened

``` 

The `;` character indicates to the shell that another command should be run
after the first command. Other options are `&&`, and `&`, they all have slightly
different sematics.

As shown we were able to run more commands than were intended. Theoretically
this could be used to download and run a malicious script.



## A solution

```python
import subprocess

def main():
    domain_name = input("Enter the domain name: ")
    command = f"nslookup '{domain_name}'"
    output = subprocess.check_output(command, shell=True, encoding="UTF-8")

    print(output)


if __name__ == '__main__':
    main()
```

This solution uses python f-strings to do the string interpolation, but more
importantly it quotes the user input to try and mitigate injections. Critically
it does not prevent injection attacks, but only makes them a bit more obscure.

A malicious input could look like this

```shell
$ python3 nslookup-fixed-take-1.py
Enter the domain name: kea.dk'; ls; echo 'oh no evil happened
Server:         10.200.10.10
Address:        10.200.10.10#53
Non-authoritative answer:
Name:   kea.dk
Address: 89.34.18.61

cryptographically-secure-randomness.py                                                            
mandatory-1.md
nslookup-invulnerable.py
nslookup-vulnerable.py
oh no evil happened

```

We were still able to inject commands, but we had to work around the quotations.
In a real environment the malicious user likely wouldn't have access to the
source code, so it would require a lot more guessing. This is sort-of a 
cat-and-mouse game, we could also try to do backslash-escaping of user-input
before executing it in the shell, but there is still another way


## A Better Solution


 ```python
 import subprocess
 
 def main():
     domain_name = input("Enter the domain name: ")
     command = ['/usr/bin/nslookup', domain_name]
     output = subprocess.check_output(command, shell=True, encoding="UTF-8")
 
     print(output)
 
 
 if __name__ == '__main__':
     main()
 ```

This solution puts the user-input in a list, thus making certain that one
argument can't be interpreted as several arguments. We also remove the 
`shell=True` paramter from the function call, I'm not sure why but it didn't
work otherwise.


∎
