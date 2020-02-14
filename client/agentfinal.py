import requests, json, psutil, platform,time,os,sys,socket
systeme = platform.system()


IP=socket.gethostbyname(socket.gethostname())
chemin = os.getcwd()+"\\init.conf"
#recuperation de l'url dans le fichier init.conf
try:
    if systeme == 'Windows' :
        with open(chemin,'r') as fichier:  
            contenu = fichier.read()
            contenu = json.loads(contenu)
            url=contenu["url"]
    elif systeme == 'Linux' :
        with open(chemin):
            contenu = fichier.read()
            contenu = json.loads(contenu)
            url=contenu["url"]        
except:
    print("fichier init.conf n'existe pas ce referé a l'administrateur")
    
chemin = os.getcwd()+"\\service.conf"    
if systeme == 'Windows' :
    if os.path.isfile(chemin):
        with open(chemin,'r')as f:
            service=f.read()
            service=json.loads(service)
    else :     
        try :
            nomaip = platform.node()+"@"+IP
            Jinit={"nom": nomaip,"os": systeme}
            reqinit=json.dumps(Jinit)
            urlinit= url+"/init"
            
            r = requests.post(urlinit,reqinit)
            contenuservice = r.json()
            with open(chemin,'w') as f:
                f.write(json.dumps(contenuservice))     
        except:
            print(sys.exc_info()[0])
            #sys.exit()
            #ae
            pass
                           
elif systeme == 'Linux' :
    if os.path.isfile(chemin):
        with open(chemin,'r')as f:
            service=f.read()
            service=json.loads(service)
    else :
        try :
            Jinit={"nom": platform.node()+"@"+IP,"os": systeme}
            reqinit=json.dumps(Jinit)
            r = requests.post(url+"/init",reqinit)
            with open(chemin,'w') as f:
                f.write(r.json())     
        except :
            print('serveur injoignable')
            sys.exit()
else :
    print('system non gérée')

    
#recherche d'un service
a = [p.name() for p in psutil.process_iter(attrs=['name'])]
if 'cmd.exe' in a :
    print ("gg")
else:
    print(a)

try:
    while(1):
        #Récupération de l'hote
        nomHost = platform.node()+IP

        #Récupération de noyau
        version = platform.release()

        #Récupération du type cpu
        cpu = platform.processor()

        #Récupération de la fréquence cpu
        cpuFre = psutil.cpu_freq().current
        cpuMax = psutil.cpu_freq().max
        if systeme == 'Windows' :
            uptime = "pas de valeur"
        elif systeme == 'Linux' :
            # calculate the uptime
            uptime_file = open('/proc/uptime')
            uptime = uptime_file.readline().split()[0]
            uptime_file.close()
            uptime = float(uptime)
            (uptime,secs) = (int(uptime / 60), uptime % 60)
            (uptime,mins) = divmod(uptime,60)
            (days,hours) = divmod(uptime,24)
            uptime = 'up %d jour%s, %d:%02d' % (days, days != 1 and 's' or '', hours, mins)

        tabDisk = []
        listdisk = psutil.disk_partitions()
        for disk in listdisk:
            if (disk.fstype != 'squashfs'):
                detaildisk = psutil.disk_usage(disk.mountpoint)
                tabDisk.append({'fileSystem':disk.device,'size':detaildisk.total,'used':detaildisk.used,'available':detaildisk.free,'pourcentage':detaildisk.percent,'mounted':disk.mountpoint})
        with open('/home/rt/test/test.txt','a')as f:
            service=f.read()
            service=json.loads(service)

        #Mémoire utilisé
        memoireused = psutil.virtual_memory().used

        #Mémoire free
        memoirefree = psutil.virtual_memory().free

        #Mémoire buffers
        memoirebuffers = psutil.virtual_memory().buffers

        #Mémoire cached
        memoirecached = psutil.virtual_memory().cached

        service["id"]=14603
        service["os"]= systeme
        service["nomhost"]= nomHost
        service["noyau"]= version
        service["cputype"]= cpu
        service["cpufrequence"]= cpuFre
        service["uptime"]=uptime
        service["metrique"]=tabDisk
        service["moccupe"]=memoireused
        service["mlibre"]=memoirefree
        service["mbuffer"]=memoirebuffers
        service["mcached"]=memoirecached
        service["total"]=memoireused+memoirefree+memoirebuffers+memoirecached
        service["cpufrequencemax"]=cpuMax
        print(service)

        donnees = json.dumps(service)
        try:
            r = requests.post(url, data=donnees)
        except:
            pass
        time.sleep(10)
except IOError:
    print(IOError)
