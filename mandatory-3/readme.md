# Cracking a simple linux user password with python and John the Ripper 


Linux user passwords are stored hashed in the so-called shadow file,
the password we need to crack looks like this
```plaintext
$6$penguins$eP.EvNiF2A.MmRVWNgGj5WSXKK8DAf7oeK8/kkbollee.F0T4KAy.QEgNAX.6wLQY1XHmSID/5VkeFiEaSA2b0
```

There are certain metadata fields incorporated into the string, each separated by a $-sign.
- The first field describes the hashing method: `6` means sha512_crypt
- The second field describes the salt, used to mitigate against pre-computed hashes for common passwords: `penguins`
- The third field is the hash: `P.EvNiF2A.MmRVWNgGj5WSXKK8DAf7oeK8/kkbollee.F0T4KAy.QEgNAX.6wLQY1XHmSID/5VkeFiEaSA2b0`


We can use the python `passlib` library to calculate a sha512_crypt compatible hash.
Iterating through all the possible password, we can try to see if we find a match.
```python
# shadow-password-cracking.py
from passlib.hash import sha512_crypt


def main():
    target = '$6$penguins$eP.EvNiF2A.MmRVWNgGj5WSXKK8DAf7oeK8/kkbollee.F0T4KAy.QEgNAX.6wLQY1XHmSID/5VkeFiEaSA2b0'    

    # We know the password is three digits, so we just loop over all the numbers up to 1000 
    for i in range(1000):

        # Pad with zeroes
        password = str(i).rjust(3, '0')
        
        hash = sha512_crypt.using(salt='penguins', rounds=5000).hash(password)
        if hash == target:
            print(f'Found password match: {password}')
            break


if __name__ == '__main__':
    main()

```


Running it looks like this:
```shell
$ python3 shadow-password-cracking.py
Found password match: 479
```


We can double check our result by trying to crack the hash with John the Ripper. Int the following we are
in a Kali Linux shell.
```plaintext
┌──(root㉿c56ada894c5a)-[~]            
└─# cat password.txt
$6$penguins$eP.EvNiF2A.MmRVWNgGj5WSXKK8DAf7oeK8/kkbollee.F0T4KAy.QEgNAX.6wLQY1XHmSID/5VkeFiEaSA2b0

┌──(root㉿c56ada894c5a)-[~]
└─# john --min-length=3 --max-length=3 --incremental=digits password.txt
Warning: detected hash type "sha512crypt", but the string is also recognized as "HMAC-SHA256"
Use the "--format=HMAC-SHA256" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 128/128 ASIMD 2x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
479              (?)
1g 0:00:00:00 DONE (2022-12-06 15:31) 2.777g/s 2133p/s 2133c/s 2133C/s 749..803
Use the "--show" option to display all of the cracked passwords reliably
Session completed.

┌──(root㉿c56ada894c5a)-[~]
└─# 

```

∎
