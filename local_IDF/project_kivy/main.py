from kivy.uix.boxlayout import BoxLayout
from kivy.app import App


# create a background class which inherits the boxlayout class
class Background(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pass


# Create App class with name of your app
class SampleApp(App):

    # return the Window having the background template.
    def build(self):
        return Background()

    # run app in the main function



if __name__ == '__main__':
    SampleApp().run()


