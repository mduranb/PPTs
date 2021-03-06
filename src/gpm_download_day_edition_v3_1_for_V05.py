#ttp://stackoverflow.com/questions/10875215/python-urllib-downloading-contents-of-an-online-directory
#ttp://stackoverflow.com/questions/4589241/downloading-files-from-an-http-server-in-python
#ttp://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
#ttp://stackoverflow.com/questions/34831770/download-a-file-in-python-with-urllib.request-instead-of-urllib
#ttp://stackoverflow.com/questions/25501090/how-to-get-wget-command-info-with-python

from urllib.request import urlopen
import http.cookiejar as cookielib

import sys
import os
import re
import string
import datetime
import urllib.request

from Login_UI import retrieveLogin

def GetNasaPermission():
    #GET NASA HTTPS DOWNLOAD PERMISSION

    GetLoginInfo = retrieveLogin()

    if GetLoginInfo != None:
        retries = 3
        while retries != 0:
            try:
                username = GetLoginInfo[0]
                password = GetLoginInfo[1]
                
                password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)
                
                cookie_jar = cookielib.CookieJar()
                
                opener = urllib.request.build_opener(
                    urllib.request.HTTPBasicAuthHandler(password_manager),
                    #urllib.request.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
                    #urllib.request.HTTPSHandler(debuglevel=1),   # details of the requests/responses
                    urllib.request.HTTPCookieProcessor(cookie_jar))
                urllib.request.install_opener(opener)
                
                LoginFailTest = urlopen('https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDF.05/2014/03/3B-DAY.MS.MRG.3IMERG.20140312-S000000-E235959.V05.nc4\n')

                print('Login successful in NASA HTTPS! WELCOME :3\n')
                
                break
    
            except:
                print('Wrong Username or Password! Please try again... You have only %d tries!!!!\n') % retries
                GetLoginInfo = retrieveLogin()
                retries -= 1
                continue
        if retries ==0:
            print('Bye');
            sys.exit(2)

    elif GetLoginInfo == None:
        print('Bye\n');
        sys.exit(2)


def gpm_day_download(input_dir, Start_Date = None,End_Date = None, backslh ='\\'):

    GetNasaPermission()

    #Get actual time
    try:
        Start_Date = list(map(int,Start_Date.split('-')))
        start_year = int(Start_Date[0])
        start_month = int(Start_Date[1])
        start_day = int(Start_Date[2])
    except:
        Start_Date = ['2014','03','12']
        start_year = '2014'
        start_month = '03'
        start_day = '12'
    try:
        End_Date =  list(map(int,(End_Date).split('-')))
        end_year = int(End_Date[0])
        end_month = int(End_Date[1])
        end_day = int(End_Date[2])
    except:
        End_Date = list(map(int,((datetime.datetime.now()).strftime('%Y-%m-%d')).split('-')))
        end_year = int(End_Date[0])
        end_month = int(End_Date[1])
        end_day = int(End_Date[2])

    
    str_Start_Date = list(map(str,Start_Date))
    str_End_Date = list(map(str,End_Date))



    #Start month
    if len(str_Start_Date[1]) == 1:
        str_Start_Date[1] = '0' + str_Start_Date[1]
    #End month
    if len(str_End_Date[1]) == 1:
        str_End_Date[1] = '0' + str_End_Date[1]

    #Start day
    if len(str_Start_Date[2]) == 1:
        str_Start_Date[2] = '0' + str_Start_Date[2]
    #End day
    if len(str_End_Date[2]) == 1:
       str_End_Date[2] = '0' + str_End_Date[2]


    #print str_Start_Date
    years = list(map(str,range(start_year,end_year+1)))

    #Download files
    try:
        for i in range(0,len(years),1):

            month = []
            months = []

            month = list(map(str,range(1,13)))

            months = list(map(lambda x: '0' + x if len(x)==1 else x,month))

            if years[i] == str_Start_Date[0]:
                try:
                    del months[:months.index(str_Start_Date[1])]
                except:
                    pass

            if years[i] == str_End_Date[0]:
                try:               
                    del months[months.index(str_End_Date[1])+1:]  
                except:
                    pass

            for j in range(0,len(months),1):
                #print months[j]
                url ='https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDF.05/'+years[i]+'/'+months[j]+'/'    
                #print url
                #Acess the URL
                try:
                    urlpath =urlopen(url)
                except:
                    continue                
                #Decode the URL
                string = urlpath.read().decode('utf-8')
                
                #Extract HDF5 files and make an file list
                pattern = re.compile('3B.*?nc4.*?')
                filelist = list(set(list(map(str,pattern.findall(string)))))
                filelist.sort()

                #print filelist
    
                try:
                    try:
                        startImg = filelist.index('3B-DAY.MS.MRG.3IMERG.'+str_Start_Date[0]+str_Start_Date[1]+str_Start_Date[2]+'-S000000-E235959.V05.nc4')
                    except:
                        startImg = filelist.index('3B-DAY.MS.MRG.3IMERG.20140312-S000000-E235959.V05.nc4')
                except:
                    startImg = None
                
                #DEL UNDER START
                if years[i] == str_Start_Date[0]:
                    if months[j] == str_Start_Date[1]:
                        #Start month
                        try:
                            del filelist[:startImg]
                        except:
                            pass
                    else:
                        pass
                else:
                    pass
                
                try:
                    endImg = filelist.index('3B-DAY.MS.MRG.3IMERG.'+str_End_Date[0]+str_End_Date[1]+str_End_Date[2]+'-S000000-E235959.V05.nc4')
                except:
                    endImg = None
                
                #print startImg,endImg,
                #print '3B-DAY.MS.MRG.3IMERG.'+str_End_Date[0]+str_End_Date[1]+str_End_Date[2]+'-S000000-E235959.V05.nc4'
                
                #DEL OVER END
                if years[i] == str_End_Date[0]:
                    if months[j] == str_End_Date[1]:    
                        #End month
                        try:
                            del filelist[endImg+1:]
                        except:
                            pass
                else:
                    pass
    
                #print filelist
    
                #Determine download block size --- default 1024 but you can up to 8192... However your files can be corrupted!
                file_size_dl = 0
                block_sz = 1024
                
                #File download poop
                for k in range(0,len(filelist),1):
                    
                    #Acess metadata and get infos
                    meta = (urlopen(url + filelist[k])).info()
                    
                    #Get file size
                    file_size = int(meta.getheaders("Content-Length")[0])
    
                    if filelist[k] in os.listdir(input_dir):
                        
                        if int(os.path.getsize(input_dir+backslh+filelist[k])) == file_size:
                            #print 'O arquivo ' + filelist[k] + ' ja existe em seu diretorio de armazenamento GPM_BRUTO e se assemelha ao mesmo arquivo do FTP de download!'
                            pass
                        else:
                            print ('O arquivo ' + filelist[k] + ' ja existe em seu diretorio de armazenamento GPM_BRUTO, porem parece estar corrompido, incompleto ou desatualizado! Baixando novamente...\n')
                            #Download message
                            print ("Downloading: %s Bytes: %s MB" % (filelist[k], str(round(float(file_size)/1000000,2))))
                            
                            #Acess file and download
                            remotefile = urlopen(url + filelist[k])
                            localfile = open(input_dir + backslh +filelist[k],'wb')
                            
                            #Download message
                            while True:
                                buffer = remotefile.read(block_sz)
                                if not buffer:
                                    break
                                file_size_dl += len(buffer)
                                localfile.write(buffer)
                                status = r"%3.3f MB  [%3.2f%%]" % ((float(file_size_dl)/1000000), file_size_dl * 100. /file_size)
                                status = status + chr(8)*(len(status)+1)
                                print (status),
                            
                            #Clear file download cache
                            file_size_dl = 0
                            
                            #Close files
                            localfile.write(remotefile.read())
                            localfile.close()
                            remotefile.close()
                    else:
    
                                        #Download message
                        print ("Downloading: %s Bytes: %s MB" % (filelist[k], str(round(float(file_size)/1000000,2))))
                        
                        #Acess file and download
                        remotefile = urlopen(url + filelist[k])
                        localfile = open(input_dir + backslh +filelist[k],'wb')
                        
                        #Download message
                        while True:
                            buffer = remotefile.read(block_sz)
                            if not buffer:
                                break
                            file_size_dl += len(buffer)
                            localfile.write(buffer)
                            status = r"%3.3f MB  [%3.2f%%]" % ((float(file_size_dl)/1000000), file_size_dl * 100. /file_size)
                            status = status + chr(8)*(len(status)+1)
                            print (status),
                        
                        #Clear file download cache
                        file_size_dl = 0
                        
                        #Close files
                        localfile.write(remotefile.read())
                        localfile.close()
                        remotefile.close()
                print ('\n')
                filelist =[]
    except:
        print ('\nDownloads finished')
    print ('\nDownloads finished')

#input_dir = r'C:\Users\Vinicius\Desktop\Teste_new_TRMM\GPM_DAY\GPM_BRUTO'

#gpm_day_download(input_dir,Start_Date='2014-12-30',End_Date='2015-01-02')

#f = open(r'C:\Users\Vinicius\Desktop\Teste_new_TRMM'+'\\' +filelist[0],'wb')    
#u = (urlopen(url + filelist[0]))
#    
#file_size_dl = 0
#block_sz = 1024
#while True:
#    buffer = u.read(block_sz)
#    if not buffer:
#        break
#
#    file_size_dl += len(buffer)
#    f.write(buffer)
#    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. /file_size)
#    status = status + chr(8)*(len(status)+1)
#    print status,
#
#f.close()
    