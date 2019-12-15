from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setWindowTitle("Scale Data Recorder")

		# 获取屏幕尺寸
		desktop=QApplication.desktop()# screen desktop
		width_scr=desktop.width() # 屏幕宽度
		height_scr=desktop.height() #屏幕高度
		self.width_scr=width_scr
		self.height_scr=height_scr

		maxheight_wd=height_scr*0.2
		maxwidth_wd=width_scr*0.4
		self.setMaximumHeight(maxheight_wd)
		self.setMaximumWidth(maxwidth_wd)
		# 设置icon
		self.setWindowIcon(QIcon('recorder.ico'))
		# 初始化UI
		self.initUi()
		# 初始化参数
		self.initParameter()

	def initParameter(self):
		pass
		

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
		self.combo_com.addItems(["COM1", "COM2", "COM3", "COM4"])
		self.combo_com.currentIndexChanged.connect(self.com_selectionchange)
		toolbar.addWidget(self.combo_com)
		toolbar.addSeparator()

		lable_baudrate=QLabel("波特率:")
		lable_baudrate.setFont(font_toolbar)
		toolbar.addWidget(lable_baudrate)
		self.combo_baudrate = QComboBox(self)
		self.combo_baudrate.addItems(["2400", "9600", "12000"])
		self.combo_baudrate.currentIndexChanged.connect(self.baudrate_selectionchange)
		toolbar.addWidget(self.combo_baudrate)
		toolbar.addSeparator()

		self.button_reco = QAction(QIcon(("startReco.png")), "启动记录", self)
		self.button_reco.setStatusTip("启动记录")
		self.button_reco.triggered.connect(self.onRecoButtonClick)

		self.button_reco.setCheckable(False)
		lable_reco=QLabel("启动记录")
		lable_reco.setFont(font_toolbar)
		toolbar.addWidget(lable_reco)
		toolbar.addAction(self.button_reco)


		lable_exp=QLabel("导出")
		lable_exp.setFont(font_toolbar)
		toolbar.addWidget(lable_exp)
		self.button_export = QAction(QIcon(("export.png")), "输出结果", self)
		self.button_export.setStatusTip("保存数据")
		self.button_export.triggered.connect(self.onExportButtonClick)
		toolbar.addAction(self.button_export)
		self.button_export.setCheckable(False)

		# statubsar
		self.setStatusBar(QStatusBar(self))

		# menu
		font_menuItem=QFont()
		font_menuItem.setPointSize(9)
		menu = self.menuBar()
		font = self.menuBar().font()
		font.setPointSize(9)
		self.menuBar().setFont(font)

		file_menu = menu.addMenu("文件")
		button_openImage = QAction(QIcon(resource_path("icons\\openFile.png")), "打开简谱图片",self)
		button_openImage.setStatusTip("打开简谱图片")
		button_openImage.setFont(font_menuItem)
		button_openImage.triggered.connect(self.onOpenFileMenu)
		button_openImage.setCheckable(False)
		file_menu.addAction(button_openImage)
		file_menu.addSeparator()

		button_feedback2 = QAction(QIcon(resource_path("icons\\feedback.png")), "反馈/更新(1)", self)
		file_menu.addAction(button_feedback2)
		button_feedback2.setFont(font_menuItem)
		button_feedback1 = QAction(QIcon(resource_path("icons\\feedback.png")), "反馈/更新(2)", self)
		file_menu.addAction(button_feedback1)
		button_feedback2.setFont(font_menuItem)
		button_feedback2.triggered.connect(lambda :self.onFeedbackClick("https://luosf.github.io/Easy-Jianpu-Trans/#"))
		button_feedback1.triggered.connect(lambda: self.onFeedbackClick("https://zhuanlan.zhihu.com/p/35889926"))

		about_menu = menu.addMenu("关于")
		button_about = QAction(QIcon(resource_path("icons\\about.png")), "关于/About", self)
		about_menu.addAction(button_about)
		button_about.setFont(font_menuItem)
		button_about.triggered.connect(self.onAboutClick)

		# layout
		widget = QWidget()
		# labelOri = QLabel("进度：", widget)
		# labelOri.move(10, 10)
		# self.pbar = QProgressBar(widget)
		# self.pbar.setGeometry(30, 40, 200, 25)
		layout=QVBoxLayout()

		font_info=QFont()
		font_info.setPointSize(9)
		self.labelFileInfo=QLabel("【简 谱】: ",widget)
		self.labelFileInfo.setFont(font_info)
		layout.addWidget(self.labelFileInfo)

		self.labelHelpInfo=QLabel(" Step 1: [文件]-[打开简谱图片]",widget)
		self.labelHelpInfo.setFont(font_info)
		layout.addWidget(self.labelHelpInfo)

		widget.setLayout(layout)
		self.setCentralWidget(widget)

	def onModifyButtonClick(self, e):
		pass
	
	def com_selectionchange(self,e):
		pass

	def baudrate_selectionchange(self,e):
		pass

	def onRecoButtonClick(self,e):
		pass


	def onOpenFileMenu(self, e):
		pass

	def onExportButtonClick(self,e):
		pass




def main():
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
