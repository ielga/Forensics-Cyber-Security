import shell
import urllib.parse

#content = "e8YB1ET3v6sm0GPyMgAp2eeiQic="

#content = urllib.parse.unquote(content)

#print(shell.decrypt(content, shell.password))

def decode_content():
    content = open("content", "r")
    log = open('logs', 'w')

    name = 'a'

    while True:
        command = content.readline()
        if not command:
            break 
        command = command.strip('\n').strip('\t')
        comm_type = content.readline().strip('\n').strip('\t')
        response = content.readline().strip('\n').strip('\t')
        content.readline()


        log.write(f"{shell.decrypt(command, shell.password)}\n")
        print(comm_type)
        decrypted = shell.decrypt(urllib.parse.unquote(response), shell.password)
        if "file" in comm_type:
            file = open(f"{name}.pdf", 'wb')
            file.write(decrypted)
            log.write(f"{name}.pdf\n\n")
            name = chr(ord(name) + 1)
        else:
            log.write(f"{decrypted}\n\n")


if __name__ == '__main__':
    decode_content()




