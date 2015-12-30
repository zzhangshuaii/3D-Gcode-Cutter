from tkinter import Tk,filedialog
#正则表达式
import re

#print(sys.argv[0])
#获取层数
def get_layer_count():
    layer_count_pos     = data.find('Layer count:')
    layer_count_pos_end = data.find('\n',layer_count_pos)
    #print(layer_count_pos)
    #print(layer_count_pos_end)
    count = data[layer_count_pos+13:layer_count_pos_end]
    return int(count)

#获得开始g代码,并替换掉g28
def get_start_gcode():
    pos = data.find(';LAYER:0')
    return data[:pos].replace('G28','')

#获取结束g代码
def get_end_gcode():
    pos = data.find('; Default end code')
    return  data[pos:]

#防止弹出一个小窗口
Tk().withdraw()

#选择文件
print('请选择gcode文件')
file_dir = filedialog.askopenfilename()
#print(file_dir)


#读取文件到data字符串
file = open(file_dir)
data = file.read()
file.close()

#获取层数
count = get_layer_count()
print('一共有0到'+str(count-1)+'层')

cut_from = input('从哪层切? 注:输入的层会被分到后半部分\n')

down = data[ : data.find(';LAYER:'+cut_from)] +get_end_gcode()

up   = get_start_gcode() + data[ data.find(';LAYER:'+cut_from)   : ]

# 取消开始移动到指定位置加热
up = up.replace('G1 Z15','')

#正则表达式 找到E的初值
re_e = re.compile('E[\d]+\.[\d]+')
se_e = re_e.search(up)
#print(se_e.group())

#G29 替换E的初值
up = up.replace('E0',se_e.group())


down_file = open(file_dir+'1.gcode','w')
down_file.write(down)
down_file.close()

up_file = open(file_dir+'2.gcode','w')
up_file.write(up)
up_file.close()

print('OK!\n切记打印之前手动回零,然后把挤出头抬升到比打印件高的地方.')
#阻止程序结束
input()
