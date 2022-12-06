import subprocess

def main():
    domain_name = input("Enter the domain name: ")

    # mitigate the risk of an injection attack, we pass the arguments as a list
    # and remove the 'shell=True' parameter.

    # If we just tried to quote the input like `command = f"nslookup '{domain_name}'"`
    # we would still be vulnerable to input like `kea.dk'; ls; echo 'oh no evil happened`

    # This strategy would require doing backslash-escaping before passing the input
    # to the function call
    
    command = ['/usr/bin/nslookup', domain_name]
    output = subprocess.check_output(command, encoding="UTF-8")

    print(output)


if __name__ == '__main__':
    main()
