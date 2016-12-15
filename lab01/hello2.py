# hello2.py
# Walker M. White (wmw2)
# August 20, 2013
"""Hello World GUI.

The purpose of this App is to test that Kivy is installed correctly."""

# Import a bunch of Kivy stuff
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.config import Config
from kivy.metrics import dp

class Panel(FloatLayout):
    """Drawing canvas to display the label.
    
    A simple Kivy panel that contains Hello World."""
    def __init__(self,**kw):
        """Constructor: Makes a new Panel for drawing shapes
        
        Precondition: **kw are Kivy key-word arguments"""
        # Pass Kivy arguments to super class.
        super(Panel,self).__init__(**kw)
        
        # Need kivy.metrics to handle retina Macs properly
        rsize = [0,0]
        rsize[0] = self.size[0]*dp(1)
        rsize[1] = self.size[0]*dp(1)
        
        # Make the background solid white
        color = Color(1.0,1.0,1.0,1.0)
        self.canvas.add(color)
        rect = Rectangle(pos=self.pos, size=rsize)
        self.canvas.add(rect)
        
        # Add the label
        label = Label(text="Hello World!")
        label.color = [0.0,0.0,0.0,1.0]
        label.size_hint = (1,1)
        label.font_size = 48*dp(1) # Again, retina Macs
        label.bold = True
        self.add_widget(label)


class HelloApp(App):
    """Primary application object.  Create and run to get the panel."""
    
    def build(self):
        """Build application with a single internal panel"""
        Config.set('graphics', 'width', '450')
        Config.set('graphics', 'height', '250')
        return Panel(size=(450,250))


# Application Code
if __name__ == '__main__':
    HelloApp().run()
