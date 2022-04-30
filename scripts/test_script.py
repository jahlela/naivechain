import subprocess as sp
from time import sleep
import requests as req
import json

nodeBase = 'http://localhost:'
nodePort_HTTP = '3001'
nodePort_P2P = '6001'
requestHeaders = {'Content-type' : 'application/json'}
processes = []
blockCounter = 0


def startNode():
  print('Starting Nodes')
  processes.append(sp.Popen(['HTTP_PORT='+nodePort_HTTP+' P2P_PORT='+nodePort_P2P+' npm start'], shell=True))
  sleep(3)
  print('Finished Starting Nodes')

def killProcs():
  for proc in processes:
    proc.terminate()
  sp.Popen(['killall node'], shell=True)

def createBlocks():
  global blockCounter
  url = nodeBase+nodePort_HTTP+'/mineBlock'
  for i in range(int(input('How many blocks would you like to create: '))):
    r = req.post(url, data=json.dumps({'data' : blockCounter}), headers=requestHeaders)
    blockCounter += 1

def getBlocks(micro=False, prnt=True, start=0, end=-1):
  if micro:
    url = nodeBase+nodePort_HTTP+'/bookmarks'
    r = req.post(url, data=json.dumps({'data': {'start': str(start), 'end': str(end)}}), headers=requestHeaders)
    if prnt: print(r.text)
    return r.text
  else:
    url = nodeBase+nodePort_HTTP+'/blocks'
    r = req.get(url)
    if prnt: print(r.text)
    return r.text

def getNumBlocks(micro=None, prnt=True):
  if micro or input('Number of microBlocks? [y/n]: ') == 'y':
    url = nodeBase+nodePort_HTTP+'/bookmarkCount'
    r = req.get(url)
    if prnt: print(r.text)
    return(int(r.text))
  else:
    url = nodeBase+nodePort_HTTP+'/blocks'
    r = req.get(url)
    if prnt: print(int(len(r.json())))
    return(int(len(r.json())))
    #print(list(i for i in json.loads(r.text)))


def getSizeOfBlocks():
  if input('Size of microBlocks? [y/n/that\'s none of your business]: ') == 'y':
    lastBlockIdx = getNumBlocks(True,False) - 1
    print(len(getBlocks(True, True, 0, lastBlockIdx)))
  else:
    print(len(getBlocks(prnt=False)))


if __name__ == '__main__':
  command = ''
  commands = {'1': createBlocks, '2': getBlocks, '3': getNumBlocks, '4': getSizeOfBlocks, '5': startNode, '6': killProcs}
  while command != '6':
    command = input("Enter a command \n  (1) to create blocks\n  (2) to get all blocks\n  (3) to get number of blocks\n  (4) to get size of blocks\n  (5) Start node\n  (6) Exit\n\nCommand: ")
    callable = commands.get(command)
    if callable is None:
      print('Error')
    else:
      callable()

  print('Script Finished')