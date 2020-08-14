#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
Created on 2020年8月14日
@author: yuejing
'''
import win32com
import xlwings as xw
from win32com.client import Dispatch
import os
import re
import os
from common import oracleSql
#https://docs.microsoft.com/zh-cn/office/vba/api/powerpoint.chart 查找相关ppt方法
#win32com.gen_py.91493440-5A91-11CF-8700-00AA0060263Bx0x2x11' has no attribute 'CLSIDToClassMap' 解决办法，删除C:\Users\yuejing\AppData\Local\Temp\gen_py\3.7下对应文件夹

#定义函数寻找负的百分比索引
def findstr(text):
	strall=[]
	#获取字符串出现的次数
	n=text.count('-')
	#获取字符串text中subStr第n次出现的位置
	def findn(text,subStr,n):
		listStr = text.split(subStr,n)
		if len(listStr) <= n:
			return -1
		return len(text)-len(listStr[-1])-len(subStr)
	#循环获取字符开始结束位置
	for i in range(1,n+1):
		a=findn(text,'-',i)
		b=text.find('%',a)+1
		strsub=[]
		strsub.append(a)
		strsub.append(b)
		strall.append(strsub)
	return strall

#读取PPT
ppt = Dispatch('PowerPoint.Application')
ppt.Visible = 1
ppt.DisplayAlerts = 0 
filepath=os.path.join(os.getcwd(), 'template/市场数据汇报.pptx')
pptSel = ppt.Presentations.Open(filepath)
slide_count=pptSel.Slides.Count

#数据库获取数据
DataDict={}
FileList=os.listdir(os.path.join(os.getcwd(), 'sql')) 	#注意文件夹中txt内容不要包含中文，否在无法识别
database=oracleSql.sqlHandle()
for file in FileList:
	DataDict[file.replace(".txt", "")]=database.sqlTxt(os.path.join(os.getcwd(), 'sql\\'+file))

#替换PPT对应表格数据，查看PPT的shape（开始->选择->选择窗格）
for i in range(1,slide_count+1):
	gen = (shape for shape in pptSel.Slides(i).Shapes)
	for item in gen:
		#PPT图表类型数据替换，PPT窗格名称与SQL文本名称一致且为图标
		if '图表' in item.Name and item.Name in DataDict:
			data = DataDict[item.Name]
			#替换PPT对应表格值
			item.Chart.ChartData.Activate()
			pwb = item.Chart.ChartData.Workbook
			pws = pwb.Sheets(1)
			pws.Cells.Rows(2).ClearContents() #清除第二行数据
			pws.Cells.Rows(3).ClearContents() #清除第三行数据
			pws.Range(pws.Cells(2,2),pws.Cells(2,2).GetOffset(len(data)-2,len(data[0])-1)).Value=[data[1],data[2]]
			pws.Range(pws.Cells(1,2),pws.Cells(1,2).GetOffset(0,len(data[0])-1)).Value=[data[0]]
			item.Chart.Refresh()
			pwb.Close()
		#PPT文本框类型数据替换，PPT窗格名称与SQL文本名称一致且为文本框
		elif '文本框' in item.Name and item.Name in DataDict:
			data =DataDict[item.Name][0]
			#获取PPT文本框
			txt = item.TextFrame.TextRange.Text
			pattern = re.compile(r'([-+]\d*\.\d\%)')
			result=pattern.split(txt)
			#替换数据
			txt = re.sub(re.escape(result[1]), data[1], txt, count=1)
			txt = re.sub(re.escape(result[3]), data[3], txt, count=1)
			txt = re.sub(re.escape(result[5]), data[5], txt, count=1)
			txt = re.sub(re.escape(result[7]), data[7], txt, count=1)
			#获取负的百分比并标红
			per=findstr(txt)
			item.TextFrame.TextRange.Text = txt
			for i in range(len(per)):
				item.TextFrame.TextRange.Characters(per[i][0],per[i][1]-per[i][0]+1).Font.Color.RGB=0xFF0000FF #ARPG

pptSel.SaveAs(os.path.join(os.getcwd(),'result/市场数据汇报.pptx'))
pptSel.Close()     #关闭打开的PowerPoint文档
ppt.Quit()         #关闭office
