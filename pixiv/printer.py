color_dic = {  # 颜色的显示字典
    'default': '#00000',
    'green': '#82D900',
    'red': '#EA0000',
    'yellow': '#EAC100',
    'blue': '#00E3E3'
}



def printer(string, color='default', style=0):
    # 对style的说明
    # 0为默认显示，1为分割线显示
    string = str(string)
    if style == 1:
        print('<font color={color}>{strMsg}</font>'.format(color=color_dic[color], strMsg=str(10 * '-' + string + 10 * '-')))
    else:
        print('<font color={color}>{strMsg}</font>'.format(color=color_dic[color], strMsg=string))
