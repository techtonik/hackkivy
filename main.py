import kivy

kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty
from kivy.network.urlrequest import UrlRequest

from glob import glob
from os.path import dirname, join, basename
from functools import partial
from time import sleep

import parsexml
import appconstants

gRoot = None
completeCurrent = False 

class RobotGuideApp(App):
	
	sound = ObjectProperty(None, allownone=True)

	@property
	def xml(self):
		if not hasattr(self, '_xml'):
			self._xml = parsexml.load_xml(appconstants.XMLFILEPATH)
		return self._xml
		
	@xml.setter
	def xml(self, path):
		self._xml = parsexml.load_xml(path)	

	@property
	def exhibits(self, index=0, name=None):
		self._exhibits = parsexml.get_exhibits(parsexml.get_excursion(self.xml, index=index, name=name))
		return self._exhibits

	@exhibits.setter
	def exhibits(self, value):
		self._exhibits = value
	@property

	def currentindex(self):
		if not hasattr(self, '_currentindex'):
			self._currentindex = 0
		return self._currentindex

	@currentindex.setter
	def currentindex(self, value):
		self._currentindex = value


	def show(self, widget=None):
		global gRoot		
		gRoot = self.root
		for wdg in self.root.children[1:]:
			self.root.remove_widget(wdg)
		if widget is None:
			widget = self.root.ids.Logo
		self.root.add_widget(widget, index=1)

        def move_to_exhibit(self, dt=0, index=None):
		global gRoot
		gRoot = self.root
		if index is None:
			index = self.currentindex

		data = self.exhibits[index]
		self.show(Image(source=data['visualurl']))

		reqstring = appconstants.HOST + '?' + str(data['x']) + '&' + str(data['y']) + '&' + str(data['phi'])
		req = UrlRequest(reqstring)

		if 0:
			self.sound = SoundLoader.load(data['audiourl'])
			## self.sound.bind(on_stop=self.sound_stop)
			# stop the sound if it's currently playing
			if self.sound.status != 'stop':
				self.sound.stop()
			else:
				self.root.ids.MainButton.text = data['description']
				self.sound.play()
				sleep(data['audiotime'])

       		if self.currentindex < len(self.exhibits) - 2:
       			self.currentindex += 1
       		else:
       			self.show()
       			self.root.ids.MainButton.text = 'Start over'
			
                #sleep(data['time'])
                # self.move_to_exhibit()
                Clock.schedule_once(self.move_to_exhibit, data['time'])
  

if __name__ == '__main__':
	RobotGuideApp().run()
