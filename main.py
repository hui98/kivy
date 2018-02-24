import kivy
import os
import socket
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import  StringProperty,AliasProperty,ObjectProperty


HOST='XXX'
PORT=XXX
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
saveroute='/storage/emulated/0/Download/'


class Root(FloatLayout):
    text1=ObjectProperty()
    text2=ObjectProperty()
    string1 = StringProperty()
    string2 = StringProperty()


    def __init__(self,**kwargs):
        super(Root, self).__init__(**kwargs)
        self.num=1
        self.checkbox1=False


    def do_action(self):
        bb=self.text1.text
        a=bb.split()
        s.sendall(bb)
        rec=s.recv(1024)
        self.text2.text+=rec+'\n'

        if rec=='Get server ready...':
            size = os.path.getsize(a[1])
            aaa = str(size).encode('utf-8')
            s.sendall(bytes(aaa))
            ok=s.recv(1024)
            if ok=='OK':
                with open (a[1]) as f:
                    for line in f:
                        s.sendall(line)
            c=s.recv(1024)
            self.text2.text+=c+'\n'

        if rec == 'Ls ready...':
            lis=s.recv(1024)
            self.text2.text+=lis+'\n'

        if rec == 'Post server ready...':
            size = s.recv(1024)
            size_str = str(size).encode('utf-8')
            s.sendall('OK')
            file_size = int(size_str)
            has_size = 0
            f = open(saveroute+a[1], 'wb')
            while True:
                if file_size == has_size:
                    f.close()
                    break
                data = s.recv(1024)
                f.write(data)
                has_size += len(data)
            self.text2.text+='Post over'+'\n'



       # s.sendall(bb)
        #data=s.recv(1024)
        #self.string2 = self.text2.text+data+'\n'
        #size = os.path.getsize("/home/hui/Pictures/hsj.jpeg")
       # aaa=str(size).encode('utf-8')
       # s.sendall(bytes(aaa))
        #print size

       # with open("/home/hui/Pictures/hsj.jpeg", "rb") as f:
           # for line in f:
              #  s.sendall(line)
    '''def do_sbprint(self):
        if self.checkbox1==False:
            print 'sb'  #when da gou run this
            self.checkbox1=True
        else:
            print'zz'
            self.checkbox1=False'''


    def show_load(self):
        content = UploadDialog(upload=self.upload, cancel=self.dismiss_popup) #there post the root proprery to the LoadDialog,and you can use root.load to callback to function Root.load()
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def upload(self, path, filename):
        fil=os.path.basename(filename[0])
        self.text1.text='post '+filename[0]+' '+fil

        '''with open(os.path.join(path, filename[0])) as stream:
            size = os.path.getsize(os.path.join(path, filename[0]))
            aaa = str(size).encode('utf-8')
            s.sendall(bytes(aaa))
            print size

            for line in stream:
                s.sendall(line)'''

        self.dismiss_popup()


    def dismiss_popup(self):
        self._popup.dismiss()


class UploadDialog(FloatLayout):
    upload = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MyApp(App):
    pass


if __name__ == '__main__':
    MyApp().run()
