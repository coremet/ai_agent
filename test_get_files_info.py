from functions.get_files_info import get_files_info

calc_curr = get_files_info("calculator", ".")
print(f'Result for current directory:\n\t{calc_curr}')

calc_pkg = get_files_info("calculator", "pkg")
print(f'''Result for 'pkg' directory:\n\t{calc_pkg}''')

calc_bin = get_files_info("calculator", "/bin")
print(f'''Result for '/bin' directory:\n\t{calc_bin}''')

calc_parent = get_files_info("calculator", "../")
print(f'''Result for '../' directory:\n\t{calc_parent}''')
