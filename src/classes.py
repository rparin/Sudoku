from ezgraphics import GraphicsImage, GraphicsWindow, ImageWindow, GraphicsMenu
import pyglet, time

class GIF:

    def __init__(self, imageFile, xLocation = 0, yLocation = 0):
        '''__init__ [Sets the image and drawing cordinates of the image]
        
        Args:
            imageFile ([string]): [The name of the image including its directory]
            xLocation (int, optional): [Where to draw the gif on the x axis]. Defaults to 0.
            yLocation (int, optional): [Where to draw the gif on the y axis]. Defaults to 0.
        '''

        #Load image file
        animation = pyglet.image.load_animation(imageFile)
        bin = pyglet.image.atlas.TextureBin()
        animation.add_to_texture_bin(bin)
        self._sprite = pyglet.sprite.Sprite(img = animation)
        
        #Create Window
        self._window = pyglet.window.Window(width=self._sprite.width, height=self._sprite.height, 
        style = pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
        self.setWin(xLocation ,yLocation)

    def setWin(self, xLocation = 0, yLocation = 0):
        '''setWin [Sets the location of the window based on input parameters]
        
        Args:
            xLocation (int, optional): [Where to draw the gif on the screen horizontally]. Defaults to 0.
            yLocation (int, optional): [Where to draw the gif on the screen vertically]. Defaults to 0.
        '''
        #Set Window location
        self._window.set_location(xLocation, yLocation)

    def play(self, seconds = 3):
        '''play [Play the gif, and how long to play it]
        
        Args:
            seconds (float, optional): [How long to play gif]. Defaults to 3.0.
        '''

        #Play gif frame by frame
        @self._window.event
        def on_draw():
            self._window.clear()
            self._sprite.draw()

        def close(event):
            self._window.close()

        #Close after x seconds
        pyglet.clock.schedule_once(close, seconds)

        #run pyglet
        pyglet.app.run()

class Animation:

    def __init__(self, imageName, frames):
        '''__init__ [Sets the image and frames of the animation]
        
        Args:
            imageName ([string]): [The name of the image]
            frames ([int]): [The amount of frames to play of image]
        '''
        self._image = imageName
        self._frames = frames

    def play(self, canvas, folder = "", xPos = 0, yPos = 0):
        '''play [Plays the animation with the specified parameters input]

        Args:
            canvas ([ezGraphics method]): [The window to play the animation]
            folder (str, optional): [Image location if image not in same directory as the program]. Defaults to "".
            xPos (int, optional): [The x location of where to display the animation]. Defaults to 0.
            yPos (int, optional): [The y location of where to display the animation]. Defaults to 0.
        '''
        for i in range(self._frames):
            directory = folder + str(self._image) + " (" + str(i+1) + ").png"
            frame = GraphicsImage(directory)
            canvas.drawImage(xPos,yPos,frame)
        
    def __repr__(self):
        '''__repr__ [Prints the image's name and the total frames input]
        
        Returns:
            [str]: [Description of the image]
        '''
        name = str(self._image) + " (" + str('number') + ").png"
        return "Image name: " + name + "\nFrames: " + str(self._frames)

class ClickBox:
    def __init__(self, xLeft, xRight, yUp, yDown):
        '''__init__ [Sets the cordinates for the box]
        
        Args:
            xLeft ([int]): [Left side of the box]
            xRight ([int]): [Right side of the box]
            yUp ([int]): [Top side of the box]
            yDown ([int]): [Bottom side of the box]
        '''
        self._xL = xLeft
        self._xR = xRight
        self._yU = yUp
        self._yD = yDown
    
    def checkBox(self, mouseClick):
        '''checkBox [Checks whether the click is in the box paramaters]
        
        Args:
            mouseClick ([string]): [string containing x and y cordinates]
        
        Returns:
            [bool]: [Returns true if mouse click is in the box, otherwise false]
        '''
        xCord = mouseClick[0]
        yCord = mouseClick[1]
        if xCord > self._xL and xCord < self._xR and yCord < self._yD and yCord > self._yU:
            return True
        else:
            return False
    
    def __repr__(self):
        '''__repr__ [Prints the box cordinatates]
        
        Returns:
            [string]: [X and y cordinates of the box]
        '''
        xCord = "xLeft: " + str(self._xL) + " xRight: " + str(self._xR)
        yCord = "\nyUp: " + str(self._yU) + " yDown: " + str(self._yD)
        return xCord + yCord

class Number:
    def __init__(self, value):
        '''__init__ [Sets the object to the value input and with a bool of a permanent]
        
        Args:
            value ([int]): [Sets the value]
        '''
        self._value = value
        self._permanent = True

    def getValue(self):
        '''getValue [Returns the value that the object holds]
        
        Returns:
            [int]: [The object's value]
        '''
        return self._value

    def setValue(self, value):
        '''setValue [Replaces the object's value with the value input]
        
        Args:
            value ([int]): [A number for the object to hold]
        '''
        self._value = value

    def setPerm(self):
        '''setPerm [Sets permanent to False]
        '''
        self._permanent = False

    def isPerm(self):
        '''isPerm [Tells user whether permanent is True or False]
        
        Returns:
            [bool]: [Returns the bool value of permanent]
        '''
        return self._permanent

    def __repr__(self):
        '''__repr__ [Prints the information of the object in dictionary form]
        
        Returns:
            [dict]: [Returns information of object]
        '''
        return str(self.__dict__)