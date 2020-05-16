#! /usr/bin/python3
import subprocess
import sys
import os.path
import time
import io
import pygame
import mailingsystem #comment this import if you don't need emails.
import emailconf

def arpscanner ():#performs arp-scan and returns result from terminal
    out = subprocess.Popen(['sudo', 'arp-scan', '-l'],
               stdout=subprocess.PIPE, 
               stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    stdout = stdout.decode('iso8859-1')
    if stderr != None:
        stderr = stderr.decode('iso8859-1')
    return stdout,stderr

def firsttimecheck():#creates and populates the files with necessary data for the first time use.
    if os.path.isfile("1list.txt") == False or os.path.isfile("2list.txt") == False or os.path.isfile("alldevices.txt") == False or os.path.isfile("spieddevices.txt") == False or os.path.isfile("unknowndevices.txt") == False:
        funknown = open("unknowndevices.txt", "a")
        funknown.close()
        fold = open("1list.txt", "w+")
        fnew = open("2list.txt", "w+")
        fspied = open("spieddevices.txt", "w+")
        fall = open("alldevices.txt", "w+")
        flog = open("log.txt", "w")
        flog.close()
        fold.seek(0)
        fnew.seek(0)
        fspied.seek(0)
        fall.seek(0)
        x=0
        while x<10:#instead of 1 arp scan, results from 10 scans will be combined. 
            stdout,stderr = arpscanner()
            if stderr==None:
                for line in stdout.split("\n"):
                    if line.startswith(emailconf.ip_beginning):
                        if line.split()[1] not in fnew.read():#checks whether this device is already in the list or not
                            fnew.seek(0, io.SEEK_END)
                            fnew.write(line+"\n")
                            fold.seek(0, io.SEEK_END)
                            fold.write(line+"\n")
                            fall.seek(0, io.SEEK_END)
                            fall.write(line+"\n")
                            fspied.seek(0, io.SEEK_END)
                            fspied.write(line+"\n")
                        fnew.seek(0)
            else:
                print(stderr)
                print("There was an issue with arp-scan. Program terminated")
                exit()
            print("Scan:", x, "done!")
            x+=1
            time.sleep(4)#ensures there's a 4 second delay between scans.
        fold.close()
        fnew.close()
        fspied.close()
        fall.close()
            
def kidsnemesis (fold, fnew):#detects which cellphone left or connected the network. it takes list of necessary devices from spieddevices.txt.
    fnew.seek(0)
    fold.seek(0)
    newread = fnew.read()
    oldread = fold.read()
    fnew.seek(0)
    fold.seek(0)
    fspied = open("spieddevices.txt", "r")
    disconnected = list()
    connected = list()
    for line in fspied:
        if len(line) < 3:#maybe when user edited textfile, he/she added empty lines. this will get rid of that issue
            continue
        if line.split()[1] in newread and line.split()[1] not in oldread:
            connected.append(''.join(str(w)+" " for w in line.split()[1:]))
    fspied.seek(0)
    for line in fspied:
        if len(line) < 3:#maybe when user edited textfile, he/she added empty lines. this will get rid of that issue
            continue
        if line.split()[1] not in newread and line.split()[1] in oldread:
            disconnected.append(''.join(str(w)+" " for w in line.split()[1:]))
    fspied.seek(0)
    return (disconnected, connected)


def comparator (fold,fnew):#compares the old and new files to see if they are different or same. Returns different or same. it takes list of all devices from alldevices.txt
    fnew.seek(0)
    fold.seek(0)
    newread = fnew.read()
    oldread = fold.read()
    fnew.seek(0)
    fold.seek(0)
    for line in fnew:
        if line.split()[1] not in oldread:
            print("Device/devices have connected since last scan")
            fnew.seek(0)
            return "different", "connected"
    for line in fold:
        if line.split()[1] not in newread:
            print("Device/devices have left since last scan")
            fold.seek(0)
            return "different", "disconnected"
    return "same", "same"

def newwriter (fnew):
    fnew.truncate(0)
    fnew.seek(0)
    x=0
    while x<10:#instead of 1 arp scan, results from 10 scans will be combined because phone wifis don't stay connected all the time. 
        stdout,stderr = arpscanner()
        if stderr==None:
            for line in stdout.split("\n"):
                if line.startswith(emailconf.ip_beginning):
                    if line.split()[1] not in fnew.read():#checks whether this device is already in the list or not
                        fnew.seek(0, io.SEEK_END)
                        fnew.write(line+"\n")
                fnew.seek(0)
        else:
            print(stderr)
            print("There was an issue with arp-scan. Program terminated")
            exit()
        print("Scan:", x, "done!")
        x+=1
        time.sleep(4)#ensures there's a 4 second delay between scans.



def matcher(fnew):#matches the scan results to known devices list.
    global unknownmailstatus
    fnew.seek(0)
    flist = open("alldevices.txt", "r")
    flistread = flist.read()
    flist.seek(0)
    flog.write("\nAll online devices:\n")
    for line in fnew:
        if len(line) < 3:#maybe when user edited textfile, he/she added empty lines. this will get rid of that issue
            continue
        flist.seek(0)
        for setir in flist:
            if len(setir) < 3:#maybe when user edited textfile, he/she added empty lines. this will get rid of that issue.
                continue
            if line.split()[1]==setir.split()[1]:
                flog.write("Currently connected:")
                w = ''.join(str(w)+" " for w in setir.split()[1:])+"\n"
                flog.write(w)
                print("Currently connected: ", ''.join(str(w)+" " for w in setir.split()[1:]))
    fnew.seek(0)
    for line in fnew:
        if line.split()[1] not in flistread:
            flog.write("Unknown connected device: ")
            w = ''.join(str(w)+" " for w in line.split()[1:])+"\n"
            flog.write(w)
            #for checking if in unknown devices list, if not, wirte it there, and inform emailing to send email.
            funknown = open("unknowndevices.txt", "r+")
            funknown.seek(0)
            if line.split()[1] not in funknown.read():
                u = ''.join(str(u)+" " for u in line.split()[:])+"\n"
                funknown.write(u)
                unknownmailstatus = 1
            funknown.close()
            print("Unkown connected device:", ''.join(str(w)+" " for w in line.split()[1:]))
    flist.close()
    fnew.seek(0)
#so that when imported, it is not run automatically
if __name__ == '__main__':
    unknownmailstatus =0    
    firsttimecheck()

    #opens files with read+write
    fold = open("1list.txt", "r+")
    fnew = open("2list.txt", "r+")
    flog = open("log.txt", "r+")
    flog.truncate(0)
    newwriter(fnew)
    compres = comparator(fold, fnew)
    if compres[0] == "different":
        #if it sees a difference between latest scan and previous one,it writes results from latest scan
        #to a file that has previous scan. So that next time when this script is run, it compares properly and knows
        #if there're any new devices.
        disconnected, connected = kidsnemesis(fold, fnew)
        if len(disconnected) !=0 or len(connected) !=0:
            flog.write("Following changes happened in Spied devices list:\n")        
        if len(disconnected) !=0:
            flog.write("\nRecently disconnected:\n")
            for w in disconnected:
                w = str(w)+"\n"
                flog.write(w)
            print("Recently disconnected:", ''.join("\n"+str(w) for w in disconnected))
        elif len(connected) !=0:
            flog.write("\nRecently connected:\n")
            for w in connected:
                w = str(w)+"\n"
                flog.write(w)
            print("Recently connected:", ''.join("\n"+str(w) for w in connected))
            pygame.mixer.quit()
            pygame.mixer.init()
            pygame.mixer.music.load(emailconf.welcoming_music)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
            pygame.mixer.quit()
        else:
            flog.write("No status change in spied devices.\n")
            print ("No status change in spied devices.")
        fnew.seek(0)
        fold.truncate(0)
        fold.seek(0)
        for line in fnew:
            fold.write(line)
        fnew.seek(0)
        fold.seek(0)
    else:
        flog.write("No change in any list detected since last check\n")
        print("No changes happened in device list since last check")

    matcher(fnew)#matches the mac addresses from newest arp scan to the list of known devices.  
    
    fold.close()
    fnew.close()
    flog.close()
    #if you don't want emails, comment all the lines below.
    #Automatically checking for new emails.
    mailingsystem.yoxla(mailingsystem.msgs)
    if compres[0] == "different":
        if len(connected) !=0 or len(disconnected) !=0 or unknownmailstatus==1:
            mailingsystem.gondergetsin()
            print("Email sent.")
