from tkinter import Tk,filedialog
import sys

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


down_file = open(file_dir+'.down.gcode','w')
down_file.write(down)
down_file.close()

up_file = open(file_dir+'.up.gcode','w')
up_file.write(up)
up_file.close()


#阻止程序结束
#input()
