from colorama import Fore, Back, Style



def main():
	print(Fore.RED + 'some red text')
	print(Back.GREEN + 'and with a green background')
	print(Style.DIM + 'and in dim text')
	print(Style.RESET_ALL)
	print('back to normal now')
	print(f'Este es un {Fore.GREEN}color{Style.RESET_ALL}')
