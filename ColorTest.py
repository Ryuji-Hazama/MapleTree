
# Console colors

Black = "\033[30m"
Red = "\033[31m"
Green = "\033[32m"
Yellow = "\033[33m"
Blue = "\033[34m"
Magenta = "\033[35m"
LightBlue = "\033[36m"
White = "\033[37m"

bgBlack = "\033[40m"
bgRed = "\033[41m"
bgGreen = "\033[42m"
bgYellow = "\033[43m"
bgBlue = "\033[44m"
bgMagenta = "\033[45m"
bgLightBlue = "\033[46m"
bgWhite = "\033[47m"

bBlack = "\033[90m"
bRed = "\033[91m"
bGreen = "\033[92m"
bYellow = "\033[93m"
bBlue = "\033[94m"
bMagenta = "\033[95m"
bLightBlue = "\033[96m"
bWhite = "\033[97m"

Bold = "\033[1m"
Underline = "\033[4m"
Reversed = "\033[7m"
Reset = "\033[0m"

# Example usage

print(f"{Black}This is black text{Reset}")
print(f"{bBlack}This is bright black text{Reset}")
print(f"{Red}This is red text{Reset}")
print(f"{bRed}This is bright red text{Reset}")
print(f"{Green}This is green text{Reset}")
print(f"{bGreen}This is bright green text{Reset}")
print(f"{Yellow}This is yellow text{Reset}")
print(f"{bYellow}This is bright yellow text{Reset}")
print(f"{Blue}This is blue text{Reset}")
print(f"{bBlue}This is bright blue text{Reset}")
print(f"{Magenta}This is magenta text{Reset}")
print(f"{bMagenta}This is bright magenta text{Reset}")
print(f"{LightBlue}This is light blue text{Reset}")
print(f"{bLightBlue}This is bright light blue text{Reset}")
print(f"{White}This is white text{Reset}")
print(f"{bWhite}This is bright white text{Reset}")
print(f"{Bold}This is bold text{Reset}")
print(f"{Underline}This is underlined text{Reset}")
print(f"{Reversed}This is reversed text{Reset}")
print(f"{bgBlack}This is text with black background{Reset}")
print(f"{bgRed}This is text with red background{Reset}")
print(f"{bgGreen}This is text with green background{Reset}")
print(f"{bgYellow}This is text with yellow background{Reset}")
print(f"{bgBlue}This is text with blue background{Reset}")
print(f"{bgMagenta}This is text with magenta background{Reset}")
print(f"{bgLightBlue}This is text with light blue background{Reset}")
print(f"{bgWhite}{Black}This is text with white background (Black text){Reset}")