import subprocess

def main():
    domain_name = input("Enter the domain name: ")
    command = "nslookup {}".format(domain_name)
    response = subprocess.check_output(command, shell=True, encoding="UTF-8")

    print(response)


if __name__ == '__main__':
    main()
