import subprocess
cmd_path = '/usr/local/bin/processing-java'
script_path = '/Users/danarmstrong/Desktop/Coursework/test/test.pde'
#a = subprocess.check_call(["processing-java", "--sketch=/Users/danarmstrong/Desktop/Coursework/test", "--run" ,"lol"])

a = subprocess.check_output([cmd_path, "--sketch=/Users/danarmstrong/Desktop/Coursework/test", "--run" ,"lol", "bob"])
print(type(a))
print(a.decode("utf-8"))
