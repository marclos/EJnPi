from pexpect import pxssh
s = pxssh.pxssh()
#     hostname = raw_input('hostname: ')
#     username = raw_input('username: ')
#     password = getpass.getpass('password: ')
#    s.login(hostname, username, password)
#    s.sendline('uptime')   # run a command
if not s.login('localhost', 'myusername', 'mypassword'):
    print("SSH session failed on login.")
    print(str(s))
else:
    s.sendline('sudo shutdown -h')
    # You may then change it to make it more suitable for you, or 
    # if needed add a second s.sendline() containing the pi password 
    # if it is asked, as you are using the sudo which normally prompts 
    # for a password.
    print("Shutdown command sent")
    s.logout()
    
