# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure(figsize=(10,7))

#fig.patch.set_facecolor('gray')

def axes_init():
  global ax1, ax2
  ax1 = fig.add_subplot(2,1,1)
  ax1.grid(True)
  ax1.set_xlim(0,20)
  ax1.set_facecolor('cornsilk')
  plt.title('Temperature[`C]',color = 'black')
  ax2 = fig.add_subplot(2,1,2)
  ax2.grid(True)
  ax2.set_xlim(0,20)
  ax2.set_facecolor('cornsilk')
  plt.title('Humidity[%]',color = 'black')

axes_init()
num = 1
xar = [num]
yar = [0]
yar2 = [0]
temp = 0
humm = 0




def on_connect(client, userdata, flags,rc):
  print('Connected with result {0}'.format(rc))
  client.subscribe('temp_room')
  client.subscribe('humm_room')

def on_message(client, userdata, msg):
  global temp, humm
  #client.publish(b"asdf",b"too")
  m = msg.payload.decode("utf-8")
  print(m)
  if msg.topic == 'temp_room':
    temp = m[6:8]
  elif msg.topic == 'humm_room':
    humm = m[6:8]
client = mqtt.Client()
client.connect('192.168.0.24',1883,60)
client.on_connect = on_connect
client.on_message = on_message

def animate(i):
  global num, xar, yar, yar2, temp, ax1, ax2
  client.loop_start()
  if num%20==0:
    ax1.clear()
    ax2.clear()
    axes_init()
    num = 0
    xar = [num]
    yar = [yar[-1]]
    yar2 = [yar2[-1]]
    num += 1
    xar.append(num)
    yar.append(temp)
    yar2.append(humm)
    if yar[0] != 0:
        ax1.plot(xar,yar,c = 'blue',ls = '--',marker = 'o', mec = 'g')
    if yar2[0] != 0:
        ax2.plot(xar,yar2,c = 'red', ls = '--',marker = 'o', mec = 'g')

  xar.pop(0)
  yar.pop(0)
  yar2.pop(0)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
