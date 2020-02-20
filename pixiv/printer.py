color_dic = {  # 颜色的显示字典
    'default': '37',
    'green': '32',
    'red': '31',
    'yellow': '33',
    'blue': '34'
}


def printer(string, color='default', style=0):
    # 对style的说明
    # 0为默认显示，1为分割线显示
    string = str(string)
    if style == 1:
        print('\033[' + color_dic[color] + 'm' + 25 * '-' + string + 25 * '-' + '\033[0m')
    else:
        print('\033[' + color_dic[color] + 'm' + string + '\033[0m')

