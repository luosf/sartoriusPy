from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import configparser
import datetime
import time
from time import gmtime, strftime
import sys
from ser import Sartorius

class RecoderWork(QThread):
	sinOut = pyqtSignal(str)

	def __init__(self,config,parent=None):
		super(RecoderWork, self).__init__(parent)
		self.parent=parent
		self.config = config
		self.working = True
		try:
			self.Sartorius=Sartorius(self.config['SERIAL']['COM'])
			self.Sartorius.set_config(config)
		except Exception as e:
			print(e)
			QMessageBox.information(self.parent, "错误", "请检查端口是否占用!")
			self.working = False
			self.exit()

	"""
		线程状态改变与终止
	"""
	def __del__(self):
		self.working = False
		self.wait()

	"""
		循环记录数据
	"""
	def run(self):
		currentTime=str_time=str(datetime.datetime.now()).split(' ')[1].replace(":",'-')
		f=open('data\\'+currentTime+".txt",'w')
		f.write('start-'+currentTime +" fps:"+self.config['COMMAND']['record_fps']+'\r\n')
		f.write('Time  mass(g)')

		while self.working == True:
			time.sleep(1.0/float(self.config['COMMAND']['record_fps']))
			#向天平读取数据 data
			data=self.Sartorius.value().decode()
			data=data.replace("\r\n",'').replace("N",'').replace(' ','').replace('[','').replace(']','').replace('g','')
			
			str_time=str(datetime.datetime.now()).split(' ')[1]
			data=str_time+"  "+data
			f.write(data+'\r\n')
			#数据返回editor窗口
			self.sinOut.emit(data)

		f.close()
		self.Sartorius.close()

	
	
class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setWindowTitle("Data Recorder || Satorious Scale")

		# 获取屏幕尺寸
		desktop=QApplication.desktop()# screen desktop
		width_scr=desktop.width() # 屏幕宽度
		height_scr=desktop.height() #屏幕高度

		self.setMinimumHeight(600)
		self.setMinimumWidth(600)
		self.setMaximumHeight(600)
		self.setMaximumWidth(600)
		# 设置icon
		self.setWindowIcon(QIcon('icons\\recorder.ico'))
		# 初始化参数
		self.initParameter()
		# 初始化UI
		self.initUi()
		

	def initParameter(self):
		self.fPath='C:\\'
		#启动的默认配置
		config = configparser.ConfigParser()
		config['SERIAL'] = {'COM':'COM1','Baudrate':9600,'bytesize':8,'parity':'serial.PARITY_ODD'}
		config['COMMAND'] = {'record_fps':1,'query':'\033P\n','zero':'\033V\n'}
		self.config=config
		#配置列表
		self.COMS = ['COM'+str(i) for i in range(18)]
		self.Baudrates = [str(i) for i in [1200,2400,4800,9600,19200] ]
		self.Bytesizes = [str(i) for i in range(1,9)]
		self.Frequencys = [str(i) for i in range(1,11)]


	def initUi(self):
		font_toolbar = QFont()
		font_toolbar.setPointSize(9)
		# toobar
		toolbar = QToolBar("my toobar")
		toolbar.setIconSize(QSize(20, 20))
		self.addToolBar(toolbar)

		lable_com=QLabel("端口:")
		lable_com.setFont(font_toolbar)
		toolbar.addWidget(lable_com)

		self.combo_com = QComboBox(self)
		self.combo_com.addItems(self.COMS)
		self.combo_com.currentIndexChanged.connect(self.com_selectionchange)
		toolbar.addWidget(self.combo_com)
		toolbar.addSeparator()

		lable_baudrate=QLabel("波特率:")
		lable_baudrate.setFont(font_toolbar)
		toolbar.addWidget(lable_baudrate)
		self.combo_baudrate = QComboBox(self)
		self.combo_baudrate.addItems(self.Baudrates)
		self.combo_baudrate.currentIndexChanged.connect(self.baudrate_selectionchange)
		toolbar.addWidget(self.combo_baudrate)
		toolbar.addSeparator()

		lable_bytesize=QLabel("数据位:")
		lable_bytesize.setFont(font_toolbar)
		toolbar.addWidget(lable_bytesize)
		self.combo_bytesize = QComboBox(self)
		self.combo_bytesize.addItems(self.Bytesizes)
		self.combo_bytesize.currentIndexChanged.connect(self.bytesize_selectionchange)
		toolbar.addWidget(self.combo_bytesize)
		toolbar.addSeparator()

		lable_recordFrequecy=QLabel("记录频率/fps")
		lable_recordFrequecy.setFont(font_toolbar)
		toolbar.addWidget(lable_recordFrequecy)
		self.combo_recordFrequecy = QComboBox(self)
		self.combo_recordFrequecy.addItems(self.Frequencys)
		self.combo_recordFrequecy.currentIndexChanged.connect(self.recordFrequecy_selectionchange)
		toolbar.addWidget(self.combo_recordFrequecy)
		toolbar.addSeparator()

		self.button_reco = QAction(QIcon(("icons\\startReco.png")), "启动", self)
		self.button_reco.setStatusTip("启动记录")
		self.button_reco.triggered.connect(self.onRecoButtonClick)

		self.button_reco.setCheckable(False)
		lable_reco=QLabel("启动")
		lable_reco.setFont(font_toolbar)
		toolbar.addWidget(lable_reco)
		toolbar.addAction(self.button_reco)

		self.button_stop = QAction(QIcon(("icons\\stop.png")), "停止", self)
		self.button_stop.setStatusTip("停止记录")
		self.button_stop.triggered.connect(self.onStopButtonClick)
		self.button_stop.setCheckable(False)
		lable_stop=QLabel("停止")
		lable_stop.setFont(font_toolbar)
		toolbar.addWidget(lable_stop)
		toolbar.addAction(self.button_stop)
		self.button_stop.setEnabled(False)

		lable_exp=QLabel("保存")
		lable_exp.setFont(font_toolbar)
		toolbar.addWidget(lable_exp)
		self.button_export = QAction(QIcon(("icons\\export.png")), "输出结果", self)
		self.button_export.setStatusTip("保存数据")
		self.button_export.triggered.connect(self.onExportButtonClick)
		toolbar.addAction(self.button_export)
		self.button_export.setCheckable(False)
		self.button_export.setEnabled(False)

		# statubsar
		self.statubsar=QStatusBar(self)
		self.setStatusBar(self.statubsar)

		# menu
		font_menuItem=QFont()
		font_menuItem.setPointSize(9)
		menu = self.menuBar()
		font = self.menuBar().font()
		font.setPointSize(9)
		self.menuBar().setFont(font)

		file_menu = menu.addMenu("文件")
		button_openConfig = QAction(QIcon(("icons\\openFile.png")), "打开配置文件",self)
		button_openConfig.setStatusTip("打开配置文件")
		button_openConfig.setFont(font_menuItem)
		button_openConfig.triggered.connect(self.onOpenFileMenu)
		button_openConfig.setCheckable(False)
		file_menu.addAction(button_openConfig)
		file_menu.addSeparator()

		button_saveConfig = QAction(QIcon(("icons\\save.png")),"保存配置文件",self)
		button_saveConfig.setStatusTip("保存配置文件")
		button_saveConfig.setFont(font_menuItem)
		button_saveConfig.triggered.connect(self.onSaveConfigFileMenu)
		button_saveConfig.setCheckable(False)
		file_menu.addAction(button_saveConfig)
		file_menu.addSeparator()

		button_feedback2 = QAction(QIcon(("icons\\feedback.png")), "反馈/更新(1)", self)
		file_menu.addAction(button_feedback2)
		button_feedback2.setFont(font_menuItem)
		button_feedback1 = QAction(QIcon(("icons\\feedback.png")), "反馈/更新(2)", self)
		file_menu.addAction(button_feedback1)
		button_feedback2.setFont(font_menuItem)
		button_feedback2.triggered.connect(lambda :self.onFeedbackClick("https://luosf.github.io/Easy-Jianpu-Trans/#"))
		button_feedback1.triggered.connect(lambda: self.onFeedbackClick("https://zhuanlan.zhihu.com/p/35889926"))

		about_menu = menu.addMenu("关于")
		button_about = QAction(QIcon(("icons\\about.png")), "关于/About", self)
		about_menu.addAction(button_about)
		button_about.setFont(font_menuItem)
		button_about.triggered.connect(self.onAboutClick)

		# layout
		widget = QWidget()

		layout=QVBoxLayout()

		font_info=QFont()
		font_info.setPointSize(9)
		
		self.labelFileInfo=QLabel("配置文件: ",widget)
		self.labelFileInfo.setFont(font_info)
		layout.addWidget(self.labelFileInfo)

		self.config_infoText='NONE'
		self.labelHelpInfo=QLabel(self.config_infoText,widget)
		self.labelHelpInfo.setFont(font_info)
		layout.addWidget(self.labelHelpInfo)

		self.editor = QPlainTextEdit(parent=widget)
		font_edit = QFont()
		font_edit.setPointSize(13)
		self.editor.setFont(font_edit)
		layout.addWidget(self.editor)

		widget.setLayout(layout)
		self.setCentralWidget(widget)

	
	def com_selectionchange(self,e):
		com=self.COMS[self.combo_com.currentIndex()]
		self.config['SERIAL']['COM']=com

	def recordFrequecy_selectionchange(self,e):
		frequency=self.Frequencys[self.combo_recordFrequecy.currentIndex()]
		self.config['COMMAND']['record_fps']=(frequency)

	def baudrate_selectionchange(self,e):
		baudrate=self.Baudrates[self.combo_baudrate.currentIndex()]
		self.config['SERIAL']['Baudrate']=baudrate

	def bytesize_selectionchange(self,e):
		bitesize=self.Bytesizes[self.combo_bytesize.currentIndex()]
		self.config['SERIAL']['bytesize']=bitesize
		
	def onStopButtonClick(self,e):
		self.thread_reco.working=False
		self.thread_reco.exit()
		self.statubsar.showMessage("记录已停止" )
		self.button_reco.setEnabled(True)
		self.button_export.setEnabled(True)
		self.button_stop.setEnabled(False)
	
	def on_recordData(self, data):
		self.record_DATA = data
		# 向editor中添加文本
		self.editor.appendPlainText(self.record_DATA)

	"""
		记录数据
	"""
	def onRecoButtonClick(self,e):
		currentTime=strftime("%Y-%m-%d %H:%M:%S", gmtime())
		self.editor.setPlainText('start :'+currentTime +" fps:"+self.config['COMMAND']['record_fps'] +"\r\nTime  mass(g)")
		self.thread_reco = RecoderWork(self.config,parent=self)
		self.thread_reco.sinOut.connect(self.on_recordData)
		self.thread_reco.start()
		self.button_reco.setEnabled(False)
		self.button_stop.setEnabled(True)
		self.button_export.setEnabled(False)


	def onOpenFileMenu(self, e):
		fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\', "Config files (*.config)")
		self.fPath = fname[0]
		if fname[0] != '':
			config = configparser.ConfigParser()
			config.read(fname[0])
			self.config=config
			
			#显示文件信息
			config_infoText = fname[0]
			self.labelHelpInfo.setText(config_infoText)

			#修改下拉选项 
			self.on_configChange_UI(self)

	def onSaveConfigFileMenu(self,e):
		# open save file Dialog
		path_Save=self.fPath.split('.')[0]
		fname_save=QFileDialog.getSaveFileName(self,"保存配置路径",path_Save,"config file (*.config )")
		if fname_save[0]!='':
			try:
				with open(fname_save[0],'w') as configFile:
					self.config.write(configFile)

				# 界面提示文字
				self.statubsar.showMessage("saved! " + fname_save[0])
			except Exception as e:
				self.statubsar.showMessage("error! 错误！" )

		

	def onExportButtonClick(self,e):
		fname_save=QFileDialog.getSaveFileName(self,"保存路径","C:\\","txt file (*.txt )")
		if fname_save[0]!='':
			try:
				data=self.editor.toPlainText()
				with open(fname_save[0],'w') as f:
					f.write(data)
			except Exception as e:
				self.statubsar.showMessage("保存出错！ 请复制数据到记事本，然后保存" )

	"""
		当config改变时，更改相应UI
	"""
	def on_configChange_UI(self,e):
		com=self.config['SERIAL']['COM']
		index_com=self.COMS.index(com)
		self.combo_com.setCurrentIndex(index_com)

		baudrate=self.config['SERIAL']['Baudrate']
		index_baudrate=self.Baudrates.index(baudrate) 
		self.combo_baudrate.setCurrentIndex(index_baudrate)

		bytesize=self.config['SERIAL']['bytesize']
		index_bytesize=self.Bytesizes.index(bytesize) 
		self.combo_bytesize.setCurrentIndex(index_bytesize)

		record_fps=self.config['COMMAND']['record_fps']

		index_record_fps=self.Frequencys.index(record_fps)
		self.combo_recordFrequecy.setCurrentIndex(index_record_fps)

		
	def onFeedbackClick(self, e):
		pass

	def onAboutClick(self,e):
		pass


def main():
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
