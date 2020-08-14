#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
Created on 2019年5月21日
@author: yuejing
'''
import xlrd
import xlwt
import yaml
import os 
from ruamel import yaml

class configyaml:
	def __init__(self,file_path):
		self.path=file_path

	def writeyaml(self,yaml_text):
		file = open(self.path, 'a', encoding='utf-8')
		yaml.dump(yaml_text, file, Dumper=yaml.RoundTripDumper)
		file.write('\n')
		file.close()

	def readyaml(self):
		abspath = os.path.dirname(os.path.abspath(__file__))
		directory=os.path.join(abspath, self.path)
		file = open(directory, 'r', encoding="utf-8")
		file_data = file.read()
		file.close()
		data = yaml.load(file_data,Loader=yaml.Loader)#yaml数据为字典或列表
		return data

class txtHandle:
	def __init__(self,file_path):
		self.path=file_path

	def readTxt(self):
		f = open(self.path,"r")
		content = f.read()
		f.close() 
		return content

	def writeTxt(self,content):
		with open(self.path,"w") as f:
			f.write(content)

class excelHandle:
	def __init__(self,file_path):
		self.path=file_path

	def excelRead(self,nread=0):
		try:
			xlbook=xlrd.open_workbook(self.path)  #打开excel
		except:
			print('路径不存在该文件！')   
		count=len(xlbook.sheets())            #获取excel工作簿数
		if nread+1>count:
			print('输入的sheet不存在\n')
		else:
			table = xlbook.sheet_by_index(nread)  # 通过索引获取工作表
			nrows = table.nrows  # 获取行数
			ncols = table.ncols  # 获取列数
			lists = []
			keys=table.row_values(0)
			for i in range(1,nrows):
				values=table.row_values(i)
				api_dict = dict(zip(keys, values))
				lists.append(api_dict)
		return lists

	def excelWrite(self,lists,nwrite=0):
		form=style()
		wt=xlwt.Workbook()
		sheet=wt.add_sheet('测试结果') 
		if len(lists)>0:
			#写入标题栏
			for t in range(len(lists[0])):
				key_value=list(lists[0].keys())
				sheet.write(0,t,key_value[t],form[0])
			# 写入列表数据
			for i in range(len(lists)):
				for j in range(len(lists[i])):
					value_list=list(lists[i].values())
					if len(str(value_list[j]))>32767:
						sheet.write(i+1, j,value_list[j][0:2000],form[1])
					else:
						sheet.write(i+1, j,value_list[j],form[1])
			wt.save(self.path)
			print('\nExcel has been written successfully!')

		else:
			print('\nlist无内容，未写入excel！')

def style():
	font = xlwt.Font() # Create the Font
	font.name = 'Times New Roman'
	font.bold = True
	#font.underline = True

	borders = xlwt.Borders()  # Create Borders
	borders.left = xlwt.Borders.DASHED
	borders.right = xlwt.Borders.DASHED
	borders.top = xlwt.Borders.DASHED
	borders.bottom = xlwt.Borders.DASHED
	borders.left_colour = 0x40
	borders.right_colour = 0x40
	borders.top_colour = 0x40
	borders.bottom_colour = 0x40

	alignment = xlwt.Alignment()  # Create Alignment
	alignment.horz = xlwt.Alignment.HORZ_CENTER #水平居中
	alignment.vert = xlwt.Alignment.VERT_CENTER #垂直居中

	pattern = xlwt.Pattern()  # Create the Pattern
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = 1 #设置单元格背景颜色

	style1 = xlwt.XFStyle()    # Create the Style
	style1.font = font         # Apply the Font to the Style
	style1.borders=borders     # Apply borders to Style
	style1.alignment=alignment # Apply alignment to Style
	style1.pattern=pattern     # Apply pattern to Style
	style1.alignment.wrap = 1  #自动换行

	style2 = xlwt.XFStyle()    # Create the Style
	style2.borders=borders     # Apply borders to Style
	style2.alignment=alignment # Apply alignment to Style
	style2.pattern=pattern     # Apply pattern to Style
	style2.alignment.wrap = 1  #自动换行
	return style1,style2


if __name__ == "__main__":
	#write
	b={'phone':{
'platformName': 'Android',
'platformVersion': [1,2,3],
'chromeOptions': {'androidProcess': 'com.tencent.mm:tools','Process': 'tools'}
}}
	conf=configyaml('config.yaml')
	conf.writeyaml(b)
	#read
	a=conf.readyaml()
	print(a['emil']['host'])