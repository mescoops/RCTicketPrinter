# import kivy module
import kivy

# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require("1.9.1")

# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App

# creates the button in kivy
# if not imported shows the error
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle
from Ticket import Ticket
from Settings import Settings


class LeftLabel(Label):
    def on_size(self, *args):
        self.text_size = self.size
        self.size_hint=(1.0, 1.0)
        self.halign="left"
        self.valign="middle"


class RightLabel(Label):
    def on_size(self, *args):
        self.text_size = self.size
        self.size_hint=(.3, None)
        self.halign="right"
        self.valign="top"

        
class TeamWidget:
    name = ""
    chkBox = None
    
    def __init__(self, name, widget):
        self.name = name
        self.chkBox = widget



class QueueItems(GridLayout):

    teams = []
 
    def __init__(self, settings, **kwargs):
        super(QueueItems, self).__init__(**kwargs)
        self.cols = 4
        
        chekSize = 50
        
        self.row_force_default = True
        self.row_default_height = chekSize
        
        first = True
        for team in settings.teams():
            teamCheck = CheckBox(group = 'queue', active = first, size_hint_x=None, width=chekSize)
            self.add_widget(teamCheck)
            self.add_widget(LeftLabel(text = team))
            self.teams.append(TeamWidget(team.upper(), teamCheck))
            first = False
            
        
    def getSelected(self) -> str:
        for team in self.teams:
            if team.chkBox.active:
                return team.name
        return 'OTHER'
        
        
class ItemEntry(GridLayout):

    def __init__(self, **kwargs):
        super(ItemEntry, self).__init__(**kwargs)
        self.cols = 2
        self.spacing = [10,0]
        
        leftSize = 200
        self.add_widget(RightLabel(text='Owner Name'))
        self.ownername = TextInput(multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.ownername)
        self.add_widget(RightLabel(text='Item'))
        self.item = TextInput(multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.item)
        self.add_widget(RightLabel(text='Problem'))
        self.problm = TextInput(size_hint_y=None, height=200)
        self.add_widget(self.problm)

        

        
class TicketApp(App):

    settings = Settings()
	
    def build(self):
        self.ticketNumber = 10
        
        self.ticketCtrl = Ticket(self.settings)
        self.qItems = QueueItems(self.settings, size_hint = (1, .4))
        self.itemItems = ItemEntry()

        rootLayout = BoxLayout(orientation='vertical')
        with rootLayout.canvas.before:
            Color(.2, .2, .2, 1)  # green; colors range from 0-1 not 0-255
            self.rect = Rectangle(size=rootLayout.size, pos=rootLayout.pos)
        rootLayout.bind(size=self._update_rect, pos=self._update_rect)
           
        rootLayout.add_widget(Label(text='Repair Café Tickets', font_size='30sp', size_hint = (1, .1)))
        rootLayout.add_widget(self.makePrintButton())
        rootLayout.add_widget(self.qItems)
        rootLayout.add_widget(self.itemItems)
        
        #self.fillTest()
        return rootLayout
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    
    def makePrintButton(self):
        btn = Button(text ="Print Ticket",
				font_size ="20sp",
				background_color =(1, 1, 1, 1),
				color =(1, 1, 1, 1),
				size =(64, 32),
				size_hint =(.4, .2),
                pos_hint = {'right': 1})

		# bind() use to bind the button to function callback
        btn.bind(on_press = self.callback)
        return btn


    def fillTest(self):
        self.itemItems.ownername.text = "Tommy Trouble"
        self.itemItems.item.text = "Toaster"
        self.itemItems.problm.text = "Toast Takes Tripple Time"

    # callback function when print button pressed
    def callback(self, event):
        self.ticketNumber += 1
        self.ticketCtrl.printTicket(self.qItems.getSelected(), self.ticketNumber, self.itemItems.ownername.text, self.itemItems.item.text, self.itemItems.problm.text)
		

root = TicketApp()
root.run()

