import subprocess

cmd_path = '/usr/local/bin/Rscript'
script_path = '/Users/danarmstrong/Desktop/Coursework/test.r'
input_text = 'abc def gea'
output = subprocess.check_output([cmd_path, script_path, input_text], universal_newlines=True)
print(output)
