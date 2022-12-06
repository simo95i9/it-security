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
