
import turtle
import time
import websockets
import psutil
import asyncio
import json

class Statistics:

    def __init__(self):
        self.ipAddr = input(" IP Address | ")
        self.port = input(" Port | ")
        self.start()
        
    def start(self):
        self.pen = turtle.Turtle()
        self.screen = turtle.Screen()
        self.canvas = self.screen.getcanvas()
        self.root = self.canvas.winfo_toplevel()
        self.root.attribute("-fullscreen", True)
        self.canvas.config(border=-2)
        self.timer = [time.time(), time.time()]
        self.pen.hideturtle()
        self.awake = False
        self.screen.bgcolor("#000000")
        self.screen.tracer(0)
        self.pen.speed(0)
        self.pen.penup()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.init())
        self.loop.run_forever()

    async def init(self):
        async with websockets.connect("ws://{}:{}".format(self.ipAddr, self.port)) as self.websocket:
            while True:
                await self.websocket.send(json.dumps({
                    "type": "request",
                    "action": "device-info"
                }))
                self.status = await self.websocket.recv()
                self.status = json.loads(self.status)
                if self.awake == False:
                    self.screen.bgcolor("#333333")
                    self.pen.color(self.status[2]["foreground"])
                    self.pen.goto(-80 + 3, 0 - (60 + 5 + 30))
                    self.pen.write("CPU Usage", font=("Calibru", 13, "bold"), align="center")
                    self.pen.goto(80 + 3, 0 - (60 + 5 + 30))
                    self.pen.write("RAM Usage", font=("Calibru", 13, "bold"), align="center")
                    self.awake = True
                else:
                    # CPU Percentage
                    self.pen.penup()
                    self.pen.goto(-80, 0)
                    self.pen.color(self.status[2]["background"][0])
                    self.pen.shape("circle")
                    self.pen.shapesize(5, 5)
                    self.pen.stamp()
                    self.pen.color(self.status[2]["background"][1])
                    for self.count in range(360):
                        self.pen.penup()
                        self.pen.goto(-80, 0)
                        self.pen.setheading((90) - self.count)
                        self.pen.fd(60)
                        self.pen.pendown()
                        self.pen.fd(5)
                        self.pen.penup()
                    self.pen.color(self.status[2]["foreground"])
                    for self.count in range(int(360 * (self.status[0]/100))):
                        self.pen.penup()
                        self.pen.goto(-80, 0)
                        self.pen.setheading(90 - self.count)
                        self.pen.fd(60)
                        self.pen.pendown()
                        self.pen.fd(5)
                        self.pen.penup()
                    self.pen.goto(-80, 0)
                    self.pen.goto(self.pen.xcor() + 3, self.pen.ycor() - 15)
                    self.pen.write("{}%".format(self.status[0]), font=("Calibri", 18, "bold"), align="center")
                    # Memory Percentage
                    self.pen.penup()
                    self.pen.goto(80, 0)
                    self.pen.color(self.status[2]["background"][0])
                    self.pen.shape("circle")
                    self.pen.shapesize(5, 5)
                    self.pen.stamp()
                    self.pen.color(self.status[2]["background"][1])
                    for self.count in range(360):
                        self.pen.penup()
                        self.pen.goto(80, 0)
                        self.pen.setheading((90) - self.count)
                        self.pen.fd(60)
                        self.pen.pendown()
                        self.pen.fd(5)
                        self.pen.penup()
                    self.pen.color(self.status[2]["foreground"])
                    for self.count in range(int(360 * (self.status[1]/100))):
                        self.pen.penup()
                        self.pen.goto(80, 0)
                        self.pen.setheading(90 - self.count)
                        self.pen.fd(60)
                        self.pen.pendown()
                        self.pen.fd(5)
                        self.pen.penup()
                    self.pen.goto(80 + 3, 0 - 15)
                    self.pen.write("{}%".format(self.status[1]), font=("Calibri", 18, "bold"), align="center")
                self.screen.update()

Statistics()
