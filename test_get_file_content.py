from functions.get_file_content import get_file_content

#trunc_logic = get_file_content("calculator", "lorem.txt") #Uncomment to test trunc logic
#print(trunc_logic)

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat")) # should return error string
print(get_file_content("calculator", "pkg/does_not_exist")) # should return error string
