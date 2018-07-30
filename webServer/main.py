# -*- coding: utf8 -*-
        
        # assetRows = getTacticDB.getRowDataFromTable('assets')
        #userProcessData =  getSthpwDB.getRowDataFromTable('login')
       # tempProjectRows = list(reversed(tempProjectRows)) #reversed
        #projectRows = tempProjectRows[-20:]

class callTactic():
      
    def __init__(self):
        import os,sys
        sys.path.append("e:/webServer/python")
        
        
        import postgreSQLCall
        reload(postgreSQLCall)


        self.getTacticDB = postgreSQLCall.callPostgre('simpleslot','postgres','','192.168.163.60','5432')  
        self.getSthpwDB = postgreSQLCall.callPostgre('sthpw','postgres','','192.168.163.60','5432')  
        self.get3DDB = postgreSQLCall.callPostgre('3D_db','postgres','','192.168.161.193','5432')  

    def getProjectDB(self):
        
        projectRows = self.getTacticDB.getRowDataFromTable('game')
        #print projectRows
        return projectRows
  
    def getProjectProcessDB(self):
        
        tempProjectInProcessRows= []
        tempProjectCompletedRows= []
        tempProjectRows = self.getTacticDB.getRowDataFromTable('game')
        for i in range(0,len(tempProjectRows)):

            if tempProjectRows[i][12] == ".In Progress":
                tempProjectInProcessRows.append(tempProjectRows[i])
            elif tempProjectRows[i][12] == ".Complete":
                tempProjectCompletedRows.append(tempProjectRows[i])
        
        return [tempProjectInProcessRows,tempProjectCompletedRows]
    
    
    
class runTactic():
    def __init__(self):
        import sys
        scripts_path = "e:/webServer/python"
        sys.path.append(scripts_path +  "/client")
        sys.path.append(scripts_path + "/scripts/tactic_scripts/ui")
        from tactic_client_lib import TacticServerStub

        self.server = TacticServerStub(setup=False)
           # tactic_server_ip = socket.gethostbyname("vg.com")


        try:
            self.tactic_server_ip = socket.gethostbyname("vg.com")
        except:
            self.tactic_server_ip = "192.168.163.60"

    

    

import os
import json
import sys


import datetime
import time
import PIL
from PIL import Image
from time import gmtime,strftime
import psycopg2
import collections
from shutil import copyfile

from flask import Flask, render_template, request

#from flask_dropzone import Dropzone
from flask import jsonify
import moviepy.editor as mp



#initial start
allowFileExtList = ['jpg','png','tif','tga','psd','mb','ma','max','3ds','json','txt','atlas','pptx','ppt','doc','xml','mp4','avi','PNG']
imageType = ['jpg','png','tif','tga','PNG','JPG','TIF','TGA']
movieClip = ['mp4','avi','mov']
dataFile = ['json','atlas']
uploadFileList = []
app = Flask(__name__)

webServerRoot = "e:/webServer"
uploadPath = webServerRoot + "/uploads" 
projectDBPath = webServerRoot +"/database/projects"
tacticProjectDBPath = "//mcd-one/database/assets/simpleslot"
projectIconPath ="e:/webServer/database/projects/projectIcons"
proJectIconURL = "http://192.168.161.193/database/projects/projectIcons"
rootURL = "http://192.168.161.193/"
spineUploadURL = "http://192.168.161.193/static/spineUpload/"
spineUploadRoot = "e:/webServer/static/spineUpload/"
#initial end

playImageList = []
playImageIndex = 0





@app.route('/getProjectSampleIcon',methods=['GET','POST'])
 
def getProjectSampleIcon():
    
   # projectInNav = request.form['projectInNav'] 
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
  #  searchKey = '\"' + projectInNav + '\"'
    cursor.execute("SELECT * FROM qc_db")
    rowData = cursor.fetchall()
    #data = reduce(filter(lambda x:x[4]== projectInNav ,rowData))
    
   # cursor = conn.cursor()
    #cursor.execute("SELECT * FROM qc_db WHERE project_name = %s"%projectInNav)
    #rowData = cursor.fetchone()
   # code = str(i)
    
    
   # print data
    
   # cursor.execute("SELECT * FROM qc_db")
   # rowData = cursor.fetchall()
    #print rowData fetchone
  #  rowCount = len(rowData)
   # print rowCount
   # code = str(i)
  #  imageList = []
   # for i in range(0,rowCount):
       # rowData[i]
    projectDict ={}
    for i in rowData:
        projectDict.update({i[4]:""})  
    #print "projectDict",projectDict
    
    
    for i in projectDict.keys():
      #  print 'ggg',i,filter(lambda x:x[4] == i and x[10] != "spineFiles" ,rowData)
        projectDict[i] = filter(lambda x:x[4] == i and x[10] != "spineFiles" ,rowData)[-1][22]
    for i in projectDict.keys():
        if projectDict[i] == 'spineFiles':
            projectDict[i] = "http://192.168.161.193:8080/database/projects/projectIcons/no_image.png"
        #print i,data[0][4]
       # print len(data)
        #if len(data) == 0:
       #     navPreviewImage = "http://192.168.161.193:8080/database/projects/projectIcons/no_image.png"
       #     projectDict[i] =navPreviewImage
       # else:
       #     projectDict[i] =data[-1][16]
        #print data[10]
    
   # for i in data:
     #   if i[10] == "spineFiles":
       #     pass
      #  else:
        #    imageList.append(i[16])
    
   # if len(imageList) == 0:
    #    navPreviewImage = "http://192.168.161.193:8080/database/projects/projectIcons/no_image.png"
   # else:
      #  navPreviewImage = imageList[-1]
    
            
     #   print i
   # print 'data',data
    data = "getProjectSampleIcon"
    return jsonify(projectDict)        




@app.route('/qcdbUpdata',methods=['POST'])
 
def qcdbUpdata():
      
    deltaTime = request.form['deltaTime']
    projectStatus = request.form['projectStatus']
    uploadLastCount = request.form['uploadLastCount']
    
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qc_db")
    qcDB = cursor.fetchall()

    conn.commit()
    conn.close()
    
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games_db")
    gameDB = cursor.fetchall()

    conn.commit()
    conn.close()
    
    currentTime = time.time()
    deltaTimeDict = {"testDeltaTime":500.0,
                     "oneDaySec":86400.0,
                     "deltaWeekTime":604800.0 ,
                     "deltaMonthTime":2592000.0,
                     "deltaYearTime":31536000.0
                     }

    projectBaseDict = {} #define file by project
    checkDeltaTime = deltaTimeDict[deltaTime]
   # print len(qcDB)
    for i in range(0,len(qcDB)):
       # print qcDB[i][4]
        if float(qcDB[i][8]) <= float(currentTime -checkDeltaTime) :
            pass
        else:
             #   if gameDB[i][0] == qcDB[i][4]:
             #       name_chn = gameDB[i][3]
             #   else:
             #       name_chn ="null"
            
            projectBaseDict.update({qcDB[i][4]:{}})
          
    for i in range(0,len(qcDB)):
        if qcDB[i][4] in projectBaseDict.keys():
            fileName = qcDB[i][1]
            try:
               # print type(fileName)
                fileInfoDict={'file_name':qcDB[i][1],
                              'file_id':qcDB[i][0],
                                'game_code':"none",
                                'name_chn':"none",
                                'icon_file':qcDB[i][16],
                                'login':qcDB[i][2],
                                'data':qcDB[i][9],
                                'tag':qcDB[i][18],
                                'description':qcDB[i][12],
                                'pc':qcDB[i][3],
                                'state_type':qcDB[i][17],
                                'retake_note_1':qcDB[i][13],
                                'retake_note_2':qcDB[i][14],
                                'retake_note_3':qcDB[i][15],
                                'file_type':qcDB[i][10],
                                'file_url':qcDB[i][21],
                                'icon_url':qcDB[i][22],
                                'asset_name':qcDB[i][23],
                                'shot_name':qcDB[i][24],
                                'meta_data':qcDB[i][11],
                                'releationship':qcDB[i][19],
                                }
                projectBaseDict[qcDB[i][4]].update({qcDB[i][0]:fileInfoDict})
            except:
                pass
            
            
    projectCount = len(projectBaseDict.keys())
    for i in range(0,projectCount):
        
        for j in range(0,len(gameDB)):
            if gameDB[j][0] == projectBaseDict.keys()[i]:
                projectBaseDict[projectBaseDict.keys()[i]]['name_chn'] = gameDB[j][3]
                projectBaseDict[projectBaseDict.keys()[i]]['game_code'] = "GAME"+"05%d"%(int(gameDB[j][1]))
                
                
    timeBaseDict = {} #define upload file by data
    timeBaseProjectList = []
    timeBaseProjectDict={}
    for i in range(0,len(qcDB)):
        timeBaseDict.update({qcDB[i][9]:{}})
        
    for i in timeBaseDict.keys():
        for project in projectBaseDict.keys():
            tempFileListInProject =[]

            timeBaseDict[i].update({project:tempFileListInProject}) 

            for j in range(0,len(qcDB)):
                if qcDB[j][9] == i and qcDB[j][4] ==project:
                    fileInfoDict= {'file_name':qcDB[j][1],
                                    'game_code':"none",
                                    'name_chn':"none",
                                    'icon_file':qcDB[j][16],
                                    'login':qcDB[j][2],
                                    'tag':qcDB[j][18],
                                    'meta_data':qcDB[j][11],
                                    'description':qcDB[j][12],
                                    'state_type':qcDB[j][17],
                                    'retake_note_1':qcDB[j][13],
                                    'meta_data':qcDB[j][14],
                                    'retake_note_2':qcDB[j][15]              
                                  }
                    timeBaseDict[i][project].append(fileInfoDict)
                if qcDB[j][4] in timeBaseProjectList:
                    pass
                else:
                    timeBaseProjectList.append(qcDB[j][4])
                    
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()   
    
    for i in timeBaseProjectList:
        searchKey = '\''+i+'\''

        code = cursor.execute("SELECT code FROM games_db WHERE name = %s"%searchKey)

    for i in range(0,len(projectBaseDict.keys())):

        print list(reversed(sorted(projectBaseDict[projectBaseDict.keys()[i]].keys())))

    
    return jsonify(projectBaseDict)

@app.route('/qcdbUpdataB',methods=['POST'])
 
def qcdbUpdataB():
  
    deltaTime = request.form['deltaTime']
    projectStatus = request.form['projectStatus']
    uploadLastCount = request.form['uploadLastCount']
    callDB  =callTactic()
    #getSthpwDB =  callDB.getSthpwDB

    get3DDB = callDB.get3DDB
    qcDB = get3DDB.getRowDataFromTable('qc_db')

    get3DDB = callDB.get3DDB
    gameDB = get3DDB.getRowDataFromTable('games_db')   
    
    
    
    currentTime = time.time()
    deltaTimeDict = {"testDeltaTime":500.0,
                     "oneDaySec":86400.0,
                     "deltaWeekTime":604800.0 ,
                     "deltaMonthTime":2592000.0,
                     "deltaYearTime":31536000.0
                     }

    projectBaseDict = {} #define file by project
    checkDeltaTime = deltaTimeDict[deltaTime]
  
    for i in range(0,len(qcDB)):

        if float(qcDB[i][8]) <= float(currentTime -checkDeltaTime) :
            pass
        else:
             #   if gameDB[i][0] == qcDB[i][4]:
             #       name_chn = gameDB[i][3]
             #   else:
             #       name_chn ="null"
                    
            projectBaseDict.update({qcDB[i][4]:{}})
    for i in range(0,len(qcDB)):
        if qcDB[i][4] in projectBaseDict.keys():
            fileInfoDict={'file_name':str(qcDB[i][1]),
                            'game_code':"none",
                            'name_chn':"none",
                            'icon_file':qcDB[i][16],
                            'login':qcDB[i][2],
                            'data':qcDB[i][9],
                            'tag':qcDB[i][18],
                            'meta_data':qcDB[i][11],
                            'description':qcDB[i][12],
                            'pc':qcDB[i][3],
                            'state_type':qcDB[i][17],
                            'retake_note_1':qcDB[i][13],
                            'retake_note_2':qcDB[i][14],
                            'retake_note_3':qcDB[i][15],
                            }
            projectBaseDict[qcDB[i][4]].update({qcDB[i][0]:fileInfoDict})
        

            
    projectCount = len(projectBaseDict.keys())
    for i in range(0,projectCount):
        
        for j in range(0,len(gameDB)):
            if gameDB[j][0] == projectBaseDict.keys()[i]:
                projectBaseDict[projectBaseDict.keys()[i]]['name_chn'] = gameDB[j][3]
                projectBaseDict[projectBaseDict.keys()[i]]['game_code'] = "GAME"+"05%d"%(int(gameDB[j][1]))
                
                
    timeBaseDict = {} #define upload file by data
    timeBaseProjectList = []
    timeBaseProjectDict={}
    for i in range(0,len(qcDB)):
        timeBaseDict.update({qcDB[i][9]:{}})
        
    for i in timeBaseDict.keys():
        for project in projectBaseDict.keys():
            tempFileListInProject =[]

            timeBaseDict[i].update({project:tempFileListInProject}) 

            for j in range(0,len(qcDB)):
                if qcDB[j][9] == i and qcDB[j][4] ==project:
                    fileInfoDict= {'file_name':qcDB[j][1],
                                    'game_code':"none",
                                    'name_chn':"none",
                                    'icon_file':qcDB[j][16],
                                    'login':qcDB[j][2],
                                    'tag':qcDB[j][18],
                                    'meta_data':qcDB[j][11],
                                    'description':qcDB[j][12],
                                    'state_type':qcDB[j][17],
                                    'retake_note_1':qcDB[j][13],
                                    'meta_data':qcDB[j][14],
                                    'retake_note_2':qcDB[j][15]              
                                  }
                    timeBaseDict[i][project].append(fileInfoDict)
                if qcDB[j][4] in timeBaseProjectList:
                    pass
                else:
                    timeBaseProjectList.append(qcDB[j][4])
    for i in timeBaseProjectList:
        searchKey = '\''+i+'\''
        code =  (get3DDB.getRowSelectDataFromTableDetial('games_db','code','name',searchKey))[0][0]
        gameCode = "GAME"+"05%d"%(int(code))
        name_chn = get3DDB.getRowSelectDataFromTableDetial('games_db','name_chn','name',searchKey)[0]
        timeBaseProjectDict.update({i:{"game_code":gameCode,"name_chn":name_chn}})
   # for i in projectBaseDict
    
                #      console.log("data2",data[1]['winner_toro_v01']['100']['file_name'])
  #
    data = {'projectBase':projectBaseDict,'timeBase':timeBaseDict,'timeBaseProjectList':timeBaseProjectDict}
                
    return jsonify(data)

   # return jsonify(projectBaseDict)



@app.route('/getProjectDB_From3DDB',methods=['POST'])

def getProjectDB_From3DDB():
    
    lastCount = -int(request.form['projectLastCount'])
    callDB  =callTactic()
    
    get3DDB = callDB.get3DDB
    projectDB_from3DDB = get3DDB.getRowDataFromTable('games_db')[lastCount:]
    #projectDB_from3DDB =lastCount
    return jsonify(projectDB_from3DDB)
    


@app.route('/testBTN_synProj',methods=['POST'])

def testBTN_synProj():
    
    
       # self.get3DDB = postgreSQLCall.callPostgre('3D_db','postgres','','192.168.161.193','5432')  

       # self.getTacticDB = postgreSQLCall.callPostgre('simpleslot','postgres','','192.168.163.60','5432')  
       # self.getSthpwDB = postgreSQLCall.callPostgre('sthpw','postgres','','192.168.163.60','5432')  
    conn = psycopg2.connect(database='simpleslot', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM game")
    rowsInTactic = cursor.fetchall()
   # conn.commit()
   # conn.close()
    
    
    conn2 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM games_db")
    rowsIn3DDB = cursor2.fetchall()
    conn2.commit()
    conn2.close()
    
    
    #totalGamesCount = len(rows)
    #allProjectList = [] 
    #allProjectFromTacticDict = {}

       # allProjectFromTacticDict
    
    indexInRowsInTactic = []
    indexInRowsIn3DDB =[]
    for i in range(0,len(rowsInTactic)):
        indexInRowsInTactic.append(rowsInTactic[i][7])

    indexInRowsInTactic = sorted(indexInRowsInTactic)       
            
    for i in range(0,len(rowsIn3DDB)):
        indexInRowsIn3DDB.append(int(rowsIn3DDB[i][1]))
    
    indexInRowsIn3DDB = sorted(indexInRowsIn3DDB)   

        
    
    notIn3DDB = filter(lambda x:x not in indexInRowsIn3DDB ,indexInRowsInTactic)
  #  conn = psycopg2.connect(database='simpleslot', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
  #  cursor = conn.cursor()
    #projectName_searchKey = '\''+projectName+'\''
    #print projectName_searchKey
   
    for i in notIn3DDB:
        #conn = psycopg2.connect(database='simpleslot', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM game WHERE id = %s"%i)
        rowData = cursor.fetchone()
        code = str(i)
        name = rowData[8]
        name_chn = rowData[10]

        game_type_code = rowData[11]
        project_status = rowData[12]
        pc = rowData[16]
        qc_dir = "e:/webServer/database/%s/qc"%name
        index = int(i)
        iconDirSource = tacticProjectDBPath +"/"+name +"/icon"
        iconFileNameSource = iconDirSource +"/"+ name +"_v001_icon.png"
        targetFileName = projectIconPath +"/"+ name +"_v001_icon.png"
        targetIconFileURL ="http://192.168.161.193:8080/database/projects/projectIcons/"+ name +"_v001_icon.png" 
        noImageURL ="http://192.168.161.193:8080/database/projects/projectIcons/no_image.png"
        #print code,name,game_type_code,project_status,pc,index,iconFileNameSource,targetFileName,targetIconFileURL
        #inputData = "\'"+code +"\'"+','+"\'"+name +"\'"+','+"\'"+game_type_code +"\'"+','+"\'"+project_status +"\'"+','+"\'"+pc +"\'"+','+"\'"+qc_dir +"\'"
        #inputData = "\'"+code +"\'"+','+"\'"+name +"\'"+','+"\'"+name_chn +"\'"+','+"\'"+game_type_code +"\'"+','+"\'"+project_status +"\'"+','+"\'"+pc +"\'"+','+"\'"+qc_dir +"\'"+','+"\'"+index +"\'"+','+"\'"+targetIconFileURL +"\'"
        conn2 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
        cursor2 = conn2.cursor()
        #inputData = "\'"+code +"\'"+','+"\'"+name +"\'"+','+"\'"+game_type_code +"\'"+','+"\'"+project_status +"\'"+','+"\'"+qc_dir +"\'"+','+"\'"+targetIconFileURL +"\'"#+','+"\'"+targetIconFileURL +"\'"
        inputData = "\'"+code +"\'"+','+"\'"+name +"\'"+','+"\'"+project_status +"\'"+','+"\'"+qc_dir +"\'"+','+"\'"+targetIconFileURL +"\'"#+','+"\'"+targetIconFileURL +"\'"

        #print 'name_chn',type(name_chn),name_chn
        #cursor2.execute( u"UPDATE games_db set project_icon_url = '%s' where id = %s;" % ( targetIconFileURL, projectNameUrl))   VALUES (%s)"%inputData)
       # cursor2.execute("INSERT INTO games_db (code,name,name_chn,game_type_code,project_status,pc,qc_dir,index,targetIconFileURL) VALUES (%s)"%inputData)
        cursor2.execute("INSERT INTO games_db (code,name,project_status,qc_dir,project_icon_url) VALUES(%s)"%inputData)
        
        #conn.commit()
        #conn.close()
    
        conn2.commit()
        conn2.close()
        
        try:
            name =  "\'"+name +"\'"
            conn2 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
            cursor2 = conn2.cursor()   
            cursor2.execute( u"UPDATE games_db set name_chn = '%s' where name = %s;" % ( name_chn, name))
            cursor2.execute( u"UPDATE games_db set pc = '%s' where name = %s;" % ( pc, name))
           # cursor2.execute( u"UPDATE games_db set pc = '%s' where name = %s;" % ( pc, index))
            commandIndex = 'UPDATE games_db SET index =' +'%s'%index +' WHERE name =' + name
            cursor2.execute(commandIndex)
            conn2.commit()
            conn2.close()
            copyfile(iconFileNameSource, targetFileName) 
        except:
            pass


        #code = cursor.execute("SELECT code FROM games_db WHERE name = %s"%searchKey)

        #if i == rowsInTactic[]
       # cursor.execute("SELECT * FROM games_db")   
    return jsonify(indexInRowsInTactic,indexInRowsIn3DDB,notIn3DDB)


            
        #cursor.execute( u"UPDATE games_db set project_icon_url = '%s' where name = %s;" % ( targetIconFileURL, projectNameUrl))













@app.route('/syncDB',methods=['POST'])

def syncDB():
    
    
    callDB  =callTactic()
    #getSthpwDB =  callDB.getSthpwDB
    get3DDB = callDB.get3DDB
    getTacticDB = callDB.getTacticDB
    #get3DDB = postgreSQLCall.callPostgre('3D_db','postgres','','192.168.161.193','5432')  
   # getTacticDB = postgreSQLCall.callPostgre('simpleslot','postgres','','192.168.163.60','5432')  
    projectRows =getTacticDB.getRowDataFromTable('game')
    getProjectState = get3DDB.getRowDataFromTable('games_db')

    #define the project list in 3d_db
    allProjectList = [] 
    allProjectFromTacticDict = {}

       # allProjectFromTacticDict

    for i in range(0,len(getProjectState)):  
        name = getProjectState[i][0]
        indexID = getProjectState[i][1]
        if name in allProjectList:
            pass
        else:
            allProjectList.append(name)
            
            

    #compare project name between tactic and 3d_db
    for i in range(0,len(projectRows)): 
        name = projectRows[i][8] 
        indexID = projectRows[i][7]
        name_chn = projectRows[i][10]
        game_type_code = projectRows[i][11]
        project_status = projectRows[i][12]
        pc = projectRows[i][16]
        qc_dir = "e:/webServer/database/%s/qc"%name
        if name in allProjectList:
            pass    
        else:
            projectInfoList = [name,name_chn,game_type_code,project_status,pc,qc_dir]
            allProjectFromTacticDict.update({indexID:projectInfoList})
        
    maxCheckCount = len(allProjectFromTacticDict.keys())
    #maxCheckCount = 10
    for i in range(0,maxCheckCount):  #len(allProjectFromTacticDict.keys)
        
        code = allProjectFromTacticDict.keys()[i]
        name = allProjectFromTacticDict[allProjectFromTacticDict.keys()[i]][0]
        name_chn = allProjectFromTacticDict[allProjectFromTacticDict.keys()[i]][1]
        game_type_code = allProjectFromTacticDict[allProjectFromTacticDict.keys()[i]][2]
        project_status = allProjectFromTacticDict[allProjectFromTacticDict.keys()[i]][3]
        pc = allProjectFromTacticDict[allProjectFromTacticDict.keys()[i]][4]
        qc_dir = allProjectFromTacticDict[allProjectFromTacticDict.keys()[i]][5]
    #    
        if name in allProjectList:
            pass
        else:
            #update and add the project name and row in table,game_db in 3d_db
            addName = "\'"+name +"\'"
            get3DDB.insertStringDataIntoTableColumn("games_db","name",addName) 
            get3DDB.updateDataToTable('games_db','name',name,'code',code)
            get3DDB.updateDataToTable('games_db','name',name,'name_chn',name_chn)
            get3DDB.updateDataToTable('games_db','name',name,'game_type_code',game_type_code)
            get3DDB.updateDataToTable('games_db','name',name,'project_status',project_status)
            get3DDB.updateDataToTable('games_db','name',name,'pc',pc)
            get3DDB.updateDataToTable('games_db','name',name,'qc_dir',qc_dir)
            
        try:
            get3DDB.updateDataToTable('games_db','name',name,'code',code)
            get3DDB.updateDataToTable('games_db','name',name,'name_chn',name_chn)
            get3DDB.updateDataToTable('games_db','name',name,'game_type_code',game_type_code)
            get3DDB.updateDataToTable('games_db','name',name,'project_status',project_status)
            get3DDB.updateDataToTable('games_db','name',name,'pc',pc)
            get3DDB.updateDataToTable('games_db','name',name,'qc_dir',qc_dir)
            
        except:
            pass

        
    #copy all project preview icon to dataBase server
    #print 'maxCheckCount',maxCheckCount
    for i in range(0,maxCheckCount):
        iconDirSource = tacticProjectDBPath +"/"+allProjectFromTacticDict.keys()[i] +"/icon"
        iconFileNameSource = iconDirSource +"/"+ allProjectFromTacticDict.keys()[i] +"_v001.png"
       # projectIconPath ="e:/webServer/database/projects/projectIcons"
        targetFileName = projectIconPath +"/"+ allProjectFromTacticDict.keys()[i] +"_v001.png"
        print 'iconFileNameSource',iconFileNameSource
       # proJectIconURL = "http://192.168.161.193/database/projects/projectIcons"
        if os.path.isfile(iconFileNameSource) == True:
            try:
                #print iconFileNameSource,targetFileName
                copyfile(iconFileNameSource, targetFileName) 
                print targetFileName
            except:
                pass
        else:
            pass
                
           
            
        
    
    return "sync finish"








def getProjectPath(projectName):
    
    projectPath = projectDBPath + "/" + projectName
    projectQCPath = projectPath + "/qc"
    projectQCIconPath = projectQCPath +"/icons"
    projectAssetsPath = projectPath +"/assets"
    projectAssetsIconsPath = projectAssetsPath +"/icons"
    projectShotsPath = projectPath +"/shots"
    projectShotsIconsPath = projectShotsPath +"/icons"



      
@app.route('/qcPreview',methods=['GET','POST'])
def qcPreview():    
    
    
    
    
    return render_template('preview_03.html')
    
 
    







    
    
    
@app.route('/getUserDB',methods=['GET','POST'])
def getUserDB():
    

    callDB  =callTactic()
    getSthpwDB =  callDB.getSthpwDB
    userDB = getSthpwDB.getRowDataFromTable('login')

    return jsonify(userDB)

    
    
    


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))

        uploadFileList.append(f.filename)
    return render_template('upload.html')


@app.route('/ggyy', methods=['POST'])
def ggyy():
    
    return "ggyy"



@app.route('/qcUpload', methods=['POST','GET'])
def qcUpload():

    app.config['UPLOADED_PATH'] = uploadPath

    for f in request.files.getlist('file'):
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        
        
    return "upload finish"


@app.route('/defineUploadFiles', methods=['POST'])
def defineUploadFiles():     
    
    fileList = request.form["sendFileList"]
    projectName = request.form["projectName"]
  
    
    
    allFileList = []
    atlasFile = []
    spineFileDict = {}
    
    tempDelFileList = []
    spineImageFileList = []

    for i in fileList.split(','):
        allFileList.append(i) #.encode("utf-8")
    
    for i in range(0,len(allFileList)):
   
        if allFileList[i].split('.')[1] == 'atlas':

            spineFileDict.update({"atlas":allFileList[i]}) 
            tempDelFileList.append(allFileList[i])
            atlasFile.append(allFileList[i])
            
        elif allFileList[i].split('.')[-1] == 'json':

            spineFileDict.update({"json":allFileList[i]}) 
            tempDelFileList.append(allFileList[i])

        elif allFileList[i].split('.')[-1] == 'skel':

            spineFileDict.update({"skel":allFileList[i]})
            tempDelFileList.append(allFileList[i])

            
    for file in atlasFile:

        atlasFileSource = uploadPath+"/"+file
 

        f = open(atlasFileSource,'r')

        for i in f.readlines():
     
            if len(i.split('\n')) == 2:
    
                if i.split('\n')[0].split('.')[-1] =='png':

                    spineImageFile = i.split('\n')[0].split('.')[0] +'.'+i.split('\n')[0].split('.')[1] 
                    tempDelFileList.append(spineImageFile)
                    spineImageFileList.append(spineImageFile)

        f.close()
    spineFileDict.update({"images":spineImageFileList})
    
        
    for file in tempDelFileList:
        allFileList.remove(file)  
        
    try:
        if len(spineFileDict['json']) >0 :
        #print ("got spine file")
            defineSpineFile(projectName,spineFileDict)
    except:
        moveFileToDataBase(projectName,allFileList)
        

    #return jsonify(spineFileDict)
    return "finish definefiles"

def defineSpineFile(projectName,spineFileDict):
    fileList = [spineFileDict['atlas'],spineFileDict['json']]
    for i in range(0,len(spineFileDict['images'])):
        fileList.append(spineFileDict['images'][i]) 
        
        
    #for i in fileList:
    #    print (i)
    sourceDir = uploadPath
    projectPath = projectDBPath + "/" + projectName
    currentDate = datetime.datetime.now().strftime('%m%d')

    projectQCPath = projectPath + "/qc"


    projectQCDatePath = projectQCPath +"/"+currentDate
    projectQCIconPath = projectQCDatePath +"/icons"
    projectAssetsPath = projectPath +"/assets"
    projectAssetsIconsPath = projectAssetsPath +"/icons"
    projectShotsPath = projectPath +"/shots"
    projectShotsIconsPath = projectShotsPath +"/icons"
    #spineUploadURL = "http://192.168.161.193/spineUpload/"
    #spineUploadRoot = "e:/webServer/static/spineUpload/"
    spineTargetProgetDir = spineUploadRoot + projectName
    spineTargetFile = spineUploadRoot + projectName +"/qc"
    spineTargetProjectDir = spineUploadRoot + projectName
    spineTargetProjectQCDir = spineTargetProjectDir +"/qc"
    spineTargetProjectQCDataDir = spineTargetProjectQCDir+'/'+currentDate
    spineTargetUrlDir = spineUploadURL + projectName + '/qc'+'/'+currentDate
   # print ('spineTargetProgetDir',spineTargetProgetDir)

    #print ('spineTargetFile',spineTargetFile)
   # print ('spineTargetProjectDir',spineTargetProjectDir)
   # print ('spineTargetProjectQCDir',spineTargetProjectQCDir)
   # print ('spineTargetProjectQCDataDir',spineTargetProjectQCDataDir)
   # print ('spineTargetUrlDir',spineTargetUrlDir)
   
    makeDirList = [projectPath,projectQCPath,projectQCDatePath,projectQCIconPath,projectAssetsPath,projectAssetsIconsPath,projectShotsPath,projectShotsIconsPath,spineTargetProgetDir,spineTargetFile,spineTargetProjectDir,spineTargetProjectQCDir,spineTargetProjectQCDataDir]
    for i in makeDirList:
        try:
            if not os.path.exists(i):
                os.makedirs(i)
        except:
            pass


    
    
    for i in fileList:#os.listdir(sourceDir):
        sourceFile =  sourceDir+"/"+i

        if os.path.isfile(sourceFile) == True: #and i.split('.')[-1] in allowFileExtList:

            targetFile = projectQCDatePath +'/'+i
            spineTargetName = spineTargetProjectQCDataDir +'/'+i
            spineFileURL = spineTargetUrlDir+'/'+i

            copyfile(sourceFile, targetFile) 
            copyfile(sourceFile, spineTargetName) 
            os.remove(sourceFile)
            #print (spineTargetName)
        else:
            pass
        
    for i in fileList:
        currentTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')

        timeStamp = time.time()
        data = currentTime.split('_')[0] 
        if i.split('.')[-1] =='json':
            registerSpineFileTODB(projectName,projectQCDatePath,i,'alpha',fileList,'%s'%timeStamp,'%s'%data,'%s'%spineTargetProjectQCDataDir,spineTargetUrlDir)
        else:
            pass

    
    
def registerSpineFileTODB(projectName,projectQCDatePath,sourcefileName,userName,fileList,timeStamp,data,spineTargetProjectQCDir,spineTargetUrlDir):
    metaData ='size%s___format(%s)___mode(%s)'%('spineFiles','spineFiles','spineFiles')
    
    fileName = spineTargetProjectQCDir +'/'+sourcefileName
    file_url =  spineTargetUrlDir+'/'+sourcefileName
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    #projectName_searchKey = '\''+projectName+'\''
    #print projectName_searchKey
    cursor.execute("SELECT * FROM games_db")
    rows = cursor.fetchall()
    iconFileName ='spineFiles'
    icon_url ='spineFiles'
    #print filter(lambda x:x[0]== projectName ,rows)[0][3] rootURL
    timestampNow = timeStamp
    nameChn = filter(lambda x:x[0]== projectName ,rows)[0][3]
    gameCode =  "GAME"+"05%d"%(int(filter(lambda x:x[0]== projectName ,rows)[0][1]))    
    fileType = 'spine'
    releationship = ""
    for i in fileList:
        releationship += (i+';')
        
    #print 'timeStamp',timeStamp
    #print 'data',data

    #print 'projectQCDatePath', projectQCDatePath      
    #print 'fileName', fileName      
    #print 'nameChn', nameChn  
    #print 'gameCode', gameCode  
    #print 'releationship',releationship
    #"SELECT %s FROM %s WHERE %s = %s"%(columnName,tableName,searchColumn,searchKey)
    inputData = "\'"+projectName +"\'"+','+"\'"+fileName +"\'"+','+"\'"+iconFileName +"\'"+','+"\'"+userName +"\'"+','+"\'"+data +"\'"+','+"\'"+timestampNow +"\'"+','+"\'"+metaData +"\'"+','+"\'"+nameChn +"\'"+','+"\'"+fileType +"\'"+','+"\'"+gameCode +"\'"+','+"\'"+file_url+"\'"+','+"\'"+icon_url +"\'"+','+"\'"+releationship +"\'"#
    #get3DDB.insertStringDataIntoTableColumn("qc_db","project_name,file_name,icon_file,login,data,timestamp,meta_data",inputData)
    #'INSERT INTO %s '%tableName + '(%s )'%columnName +'VALUES '+'('+ value +')'
    cursor.execute("INSERT INTO qc_db (project_name,file_name,icon_file,login,data,timestamp,meta_data,name_chn,file_type,game_code,file_url,icon_url,releationship) VALUES (%s)"%inputData)
    conn.commit()
    conn.close()
    #print inputData
    
    
    
    
    


def moveFileToDataBase(projectName,fileList):
    sourceDir = uploadPath
    projectPath = projectDBPath + "/" + projectName
    currentDate = datetime.datetime.now().strftime('%m%d')

    projectQCPath = projectPath + "/qc"

    
    projectQCDatePath = projectQCPath +"/"+currentDate
    projectQCIconPath = projectQCDatePath +"/icons"
    projectAssetsPath = projectPath +"/assets"
    projectAssetsIconsPath = projectAssetsPath +"/icons"
    projectShotsPath = projectPath +"/shots"
    projectShotsIconsPath = projectShotsPath +"/icons"

    makeDirList = [projectPath,projectQCPath,projectQCDatePath,projectQCIconPath,projectAssetsPath,projectAssetsIconsPath,projectShotsPath,projectShotsIconsPath]
    for i in makeDirList:
        try:
            if not os.path.exists(i):
                os.makedirs(i)
        except:
            pass
        
    #print "movie code check 0"
   
    for i in fileList:#os.listdir(sourceDir):
        sourceFile =  sourceDir+"/"+i

        if os.path.isfile(sourceFile) == True: #and i.split('.')[-1] in allowFileExtList:

            targetFile = projectQCDatePath +'/'+i

            copyfile(sourceFile, targetFile) 
            os.remove(sourceFile)

            if targetFile.split('.')[-1] in imageType:
                createIcon(projectName,i,projectQCDatePath) 
            elif targetFile.split('.')[-1] in movieClip:
                #print "movie code check 0.1"
                currentTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                data = currentTime.split('_')[0]
                #print i
                timeStamp = time.time()
                sourceFileName = projectQCDatePath +'/'+i
               # print "sourceFileName",sourceFileName

                newName = projectQCDatePath +'/'+projectName+'_'+currentTime+'.'+i.split('.')[-1]
                os.rename(sourceFileName,newName)
             #   print "newName",newName

                createMovieIcon(projectName,newName,projectQCDatePath,currentTime,data,timeStamp) 


            else:
                pass
                
    


def createMovieIcon(currentProjectSelect,fileName,sourceDir,currentTime,data,timeStamp):
    sourceFileName =fileName
   # print 'sourceFileName',sourceFileName
   # print 'currentProjectSelect',currentProjectSelect
   # currentTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
   # data = currentTime.split('_')[0]
   # timeStamp = time.time()
    #iconMovieName = sourceDir + "/icons/" +currentProjectSelect+"_icon_"+currentTime+'.'+fileName.split('.')[-1]
    iconMovieName = sourceDir + "/icons/" +currentProjectSelect+"_icon_"+currentTime+'.gif'
   # print "movie code check 1"
    clip = mp.VideoFileClip(sourceFileName)
  #  print "movie code check 2"
   # print "newName",newName
    clipSize = clip.size
    clipDuration = clip.duration
    clipFps = clip.fps
    metaData ='size%s___fps(%s)___duration(%s)'%(clipSize,clipFps,clipDuration)
    registerToQCDB("%s"%currentProjectSelect,"%s"%sourceFileName,"%s"%iconMovieName,"alpha","%s"%data,"%s"%timeStamp,"%s"%metaData)

    clip_resized = clip.resize(width=200) 
    #clip_resized.write_videofile(iconMovieName)
    clip_resized.write_gif(iconMovieName, fps=3)

    
    
    
def createIcon(currentProjectSelect,fileName,sourceDir):
    sourceFileName = sourceDir +'/'+fileName
    currentTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    timeStamp = time.time()

    data = currentTime.split('_')[0]
    iconName = sourceDir + "/icons/" +currentProjectSelect+"_icon_"+currentTime+'.'+fileName.split('.')[-1]
    im = Image.open( sourceFileName )
    imageFormat = im.format
    imageSize = im.size
    imageMode = im.mode
    metaData ='size%s___format(%s)___mode(%s)'%(imageSize,imageFormat,imageMode)
    #'%s+%s'%(rootURL,fileName.split('e:/webServer/')[1])
    registerToQCDB("%s"%currentProjectSelect,"%s"%sourceFileName,"%s"%iconName,"alpha","%s"%data,"%s"%timeStamp,"%s"%metaData)

    width = 200
    ratio = float(width)/im.size[0]
    height = int(im.size[1]*ratio)

    createIcon = im.resize( (width, height), Image.BILINEAR )
    createIcon.save( iconName )





def registerToQCDB(projectName,fileName,iconFileName,userName,data,timestamp,metaData):
    #conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    #cursor = conn.cursor()
    
    #print filter(lambda x:x[0]== 176 ,rows)

    file_url = "http://192.168.161.193:8080/%s"%(fileName.split('e:/webServer/')[1])
    icon_url = "http://192.168.161.193:8080/%s"%(iconFileName.split('e:/webServer/')[1])
    #print 'sdsdsdsdsdsds',iconFileName.split('e:/webServer/')[1] ,type(iconFileName.split('e:/webServer/')[1])
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    #projectName_searchKey = '\''+projectName+'\''
    #print projectName_searchKey
    cursor.execute("SELECT * FROM games_db")
    rows = cursor.fetchall()
    
    #print filter(lambda x:x[0]== projectName ,rows)[0][3] rootURL
    
    nameChn = filter(lambda x:x[0]== projectName ,rows)[0][3]
    gameCode =  "GAME"+"05%d"%(int(filter(lambda x:x[0]== projectName ,rows)[0][1]))
    #print 'sdsadsadsa',fileName.split('e:/webServer/')[1], type(fileName.split('e:/webServer/')[1])
    
    
    
    #print "fileURL",file_url,type(file_url)
   # icon_url= str(rootURL+iconFileName.split('e:/webServer/')[1])
  #  print "iconURL",icon_url
    try:
        extName = fileName.split('.')[-1]
        if extName in imageType :
            fileType =  'image' 
        elif extName in movieClip :
            fileType =  'movieClip'
        elif extName in dataFile:
            fileType =  'dataFile'


        
    except:
        pass
    
    #"SELECT %s FROM %s WHERE %s = %s"%(columnName,tableName,searchColumn,searchKey)
    inputData = "\'"+projectName +"\'"+','+"\'"+fileName +"\'"+','+"\'"+iconFileName +"\'"+','+"\'"+userName +"\'"+','+"\'"+data +"\'"+','+"\'"+timestamp +"\'"+','+"\'"+metaData +"\'"+','+"\'"+nameChn +"\'"+','+"\'"+fileType +"\'"+','+"\'"+gameCode +"\'"+','+"\'"+file_url+"\'"+','+"\'"+icon_url +"\'"#
    #get3DDB.insertStringDataIntoTableColumn("qc_db","project_name,file_name,icon_file,login,data,timestamp,meta_data",inputData)
    #'INSERT INTO %s '%tableName + '(%s )'%columnName +'VALUES '+'('+ value +')'
    cursor.execute("INSERT INTO qc_db (project_name,file_name,icon_file,login,data,timestamp,meta_data,name_chn,file_type,game_code,file_url,icon_url) VALUES (%s)"%inputData)
    conn.commit()
    conn.close()
    


    
def registerToQCDB_B(projectName,fileName,iconFileName,userName):

    project_name =""
    game_code = ""
    asset_code =""
    shot_code = ""
    data = ""
    timestamp =""
    login =""
    meta_data=""
    file_type=""
    file_name=" "
    
    
    return "dbTest"
    
    
    
 






    
    


@app.route('/projectMain')
def projectMain():
    
    
  #  callDB  =callTactic()
   # return "project Main"
    return render_template('main.html')







@app.route('/requireQCDB', methods=['POST', 'GET'])
def requireQCDB():
    
    
    callDB  =callTactic()
    get3DDB =  callDB.get3DDB
    qcdb =  get3DDB.getRowDataFromTable('qc_db')
    

    return "require QCDB"









@app.route('/completed')
def completed():

    uploadFileList = []




@app.route('/pixiSpine')
def pixiSpine():
    bgList = ["bg.png","BG.png","Bg.png","bg.jpg","BG.jpg","Bg.jpg"]
    if len(uploadFileList) == 0:
        pass
    else:
        bgImage = "none"
        for i in uploadFileList:
            if i.split(".")[1] == "json":
                spineJson = i
            elif i.split(".")[1] == "png":
                spineSpriteImage = i
            elif i.split(".")[1] == "atlas":
                spineSpriteAtlas = i
            elif i in bgList:
                bgImage = i

           # data = "test test test"
        effectName = getEffectName(spineJson)
        
        return render_template('pixiSpine.html',uploadFileList= uploadFileList, effectName = effectName,spineJson=spineJson,bgImage = bgImage )
    
 ###

@app.route('/hello/')
def hello():
    return render_template('hello.html')




@app.route('/pixiJsonLoad', methods=['GET', 'POST'])
def pixiJsonLoad():
    pixiJsonFile = request.form["pixiJsonFile"]
    fileID = request.form["fileID"]
    fileUrl = request.form["fileUrl"]
    print 'pixiJsonFile',pixiJsonFile
    
    with open(pixiJsonFile) as data_file:    
        pixiJsonData = json.load(data_file)
        
    pixiAnimationList = pixiJsonData['animations'].keys()
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qc_db")
    rows = cursor.fetchall()

    getReleationship = filter(lambda x:x[0]== int(fileID) ,rows)[0][19]
    fileLocation = filter(lambda x:x[0]== int(fileID) ,rows)[0][1]
    atlasFile = filter(lambda x:x.split('.')[-1]== 'atlas' ,getReleationship.split(';'))[0]
    jsonFIle = filter(lambda x:x.split('.')[-1]== 'json' ,getReleationship.split(';'))[0]
    atlasFullName = fileLocation.split(jsonFIle)[0] +atlasFile
    descriptionText = filter(lambda x:x[0]== int(fileID) ,rows)[0][12]

    f = open(atlasFullName,'r')

    for i in f.readlines()[0:3]:
        
        if i.split(':')[0] == 'size':
            
            imageSizr = i.split(':')[1]
            
            
            
     
    conn.commit()
    conn.close()

    return jsonify(pixiJsonData,fileID,fileUrl,imageSizr,descriptionText)





@app.route('/cleanReq/',methods=['POST','GET'])
def cleanReq():
    
    uploadFileList = []
    name=request.form.get('name')

    return name



##AJAX test  Start####    
@app.route('/jqTest',methods=['POST','GET'])
def jqTest():
    
    return render_template('jqTestImport.html')






@app.route('/sync_icons',methods=['GET','POST'])
def sync_icons():
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games_db")
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    projectCount = len(rows)
    data = list(reversed(sorted(rows, key = lambda x: int(x[1]))))
    progressProject = filter(lambda x:x[4]==".In Progress",data)
    maxCheckCount = len(progressProject)
    
    for i in range(0,maxCheckCount):
        iconDirSource = tacticProjectDBPath +"/"+progressProject[i][0] +"/icon"
        iconFileNameSource = iconDirSource +"/"+ progressProject[i][0] +"_v001_icon.png"
        targetFileName = projectIconPath +"/"+ progressProject[i][0] +"_v001_icon.png"
        
        #name ='\"'+ progressProject[i][0] +'\"'
        name =progressProject[i][0]
       # print name

   # print 'iconFileNameSource',iconFileNameSource
        if os.path.isfile(iconFileNameSource) == True:
            try:
                #print iconFileNameSource,targetFileName
                copyfile(iconFileNameSource, targetFileName) 
                conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
                cursor = conn.cursor()
                iconUrl = "http://192.168.161.193:8080/database/projects/projectIcons/"+ progressProject[i][0] +"_v001_icon.png"
                cursor.execute( u"UPDATE games_db set project_icon_url = '%s' where name = '%s';" % ( iconUrl, name))
                conn.commit()
                conn.close()

                
                
                
                
            except:
                pass
        else:
            pass

        if os.path.isfile(targetFileName) == True:
            pass
        else:
            
            conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
            cursor = conn.cursor()
            iconUrl = "http://192.168.161.193:8080/database/projects/projectIcons/no_image.png"
            cursor.execute( u"UPDATE games_db set project_icon_url = '%s' where name = '%s';" % ( iconUrl, name))
            conn.commit()
            conn.close()

    
    return jsonify(maxCheckCount,progressProject)



##"送出專案資料，由3dDB games_db中取得資料"



@app.route('/getProjectProcessDB',methods=['GET'])
def getProjectProcessDB():
    
    
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games_db")
    rows = cursor.fetchall()

    data ="finished"
    projectCount = len(rows)

    data = list(reversed(sorted(rows, key = lambda x: int(x[1]))))
    progressProject = filter(lambda x:x[4]==".In Progress",data)
    
    return jsonify(progressProject)
    

    
@app.route('/getProjectCompletedDB',methods=['GET'])
def getProjectCompletedDB():
    
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games_db")
    rows = cursor.fetchall()

    data ="finished"
    projectCount = len(rows)

    data = list(reversed(sorted(rows, key = lambda x: int(x[1]))))
    completeProject = filter(lambda x:x[4]==".Complete",data)

        
        
    return jsonify(completeProject)

        
@app.route('/getProjectRecentDB',methods=['GET'])
def getProjectRecentDB():
    
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games_db")
    rows = cursor.fetchall()

    data ="finished"
    projectCount = len(rows)

    data = list(reversed(sorted(rows, key = lambda x: int(x[1]))))

        
        
    return jsonify(data)

    
    



@app.route("/indexPage",methods=['POST','GET'])
def indexPage():
    app.config['UPLOADED_PATH'] = os.getcwd() + '/upload'
    return render_template('indexPageTest.html')



@app.route('/dropzoneUploadTest', methods=['GET', 'POST'])
def upload_file():
    
    app.config['UPLOADED_PATH'] ="e:/webServer/uploads"
    if request.method == 'POST':
        for f in request.files.getlist('file'):
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('dropzoneUploadTest.html')





@app.route('/qc', methods=['GET', 'POST'])
def qclist():
    
    app.config['UPLOADED_PHOTOS_DEST']="//mcd-one/3d_project/temp"
    files_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
    return render_template('qclist28.html', files_list=files_list)


@app.route('/qcMain', methods=['GET', 'POST'])
def qcMain():
    
    #app.config['UPLOADED_PHOTOS_DEST']="//mcd-one/3d_project/temp"
    #files_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
    return render_template('qcMain.html')






@app.route('/scriptLinkTest', methods=['GET', 'POST'])
def scriptLinkTest():
    
    return render_template('scriptLinkTest.html') 

##AJAX test####    

    
        
def getEffectName(jsonFile):
    path = 'c:/webServer/static/uploads/'
    fileName = path + jsonFile

    with open(fileName) as data_file:    
        data = json.load(data_file)
    return data["animations"].keys()[0]



### learning map , table
@app.route('/learning')
def learningMap():
    
    
    
   # return "learning Map" registClass 
    return render_template('learningMap3.html ')
    

@app.route('/learning2')
def learningMap2():
    
    
    
   # return "learning Map" registClass 
    return render_template('learningMap2.html ')
        
    
    
    
### learning map , table

    
@app.route('/registClass',methods=['GET','POST'])
def registClass():
    
    className = (request.form['className']).encode("utf-8")
    classDescription = (request.form['classDescription']).encode("utf-8")
    
   

    callDB  =callTactic()
    get3DDB =  callDB.get3DDB
    getTacticDB = callDB.getTacticDB



    inputData = "\'"+className.decode("utf-8") +"\'"+','+"\'"+classDescription.decode("utf-8") +"\'"
    get3DDB.insertStringDataIntoTableColumn("learning_map","lesson_name,description",inputData)


    return" regist class finish"
    
    
@app.route('/getExistLearnTable',methods=['GET','POST'])
def getExistLearnTable():
    
    
    callDB  =callTactic()
    get3DDB =  callDB.get3DDB
    learning_mapDB = get3DDB.getRowDataFromTable('learning_map')
    classDB = {}
    classIndexList=[]
    for i in range(0,len(learning_mapDB)):
        if learning_mapDB[i][0] in classIndexList:
            pass
        else:
            classIndexList.append(learning_mapDB[i][0])
    classIndexList = sorted(classIndexList)
    for i in classIndexList:
        classDB.update({str(i):{}})
        
    for i in range(0,len(learning_mapDB)):
        keyValue = str(learning_mapDB[i][0])
        classDB[keyValue].update({"lessonName":learning_mapDB[i][1]})
        classDB[keyValue].update({"lennonType":learning_mapDB[i][2]})
        classDB[keyValue].update({"tag":learning_mapDB[i][3]})
        classDB[keyValue].update({"teacher":learning_mapDB[i][4]})
        classDB[keyValue].update({"description":learning_mapDB[i][5]})
        classDB[keyValue].update({"releationshipClass":learning_mapDB[i][6]})
        classDB[keyValue].update({"requirement":learning_mapDB[i][7]})
        classDB[keyValue].update({"already_study":learning_mapDB[i][8]})
        classDB[keyValue].update({"class_level":learning_mapDB[i][9]})
        classDB[keyValue].update({"clsss_grade":learning_mapDB[i][10]})

    
    
    data = "getExistLearnTable close"
    return jsonify(classDB)
    

    
@app.route('/delClassElement',methods=['GET','POST'])
def delClassElement():
    
    
    callDB  =callTactic()
    get3DDB =  callDB.get3DDB


    learning_mapDB = get3DDB.getRowDataFromTable('learning_map')
    classElement = request.form['classElement']
    inputData = classElement
    get3DDB.deleteRowFromSearchKey('learning_map','index',inputData)
    data = "delClassElement close"
    return jsonify(data)
    



@app.route('/addTagToItem',methods=['GET','POST'])
def addTagToItem():
    
    
    callDB  =callTactic()
    get3DDB =  callDB.get3DDB


    learning_mapDB = get3DDB.getRowDataFromTable('learning_map')
    tagListItems = request.form['tagListItems']
    tagListID =  request.form['tagListID']
    classIndex = str(tagListID.split('_')[1])
 
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()

    cursor.execute( u"UPDATE learning_map set tag = '%s' where index = %s;" % ( tagListItems, classIndex))

    conn.commit()
    conn.close()

    data = "update tag to DB"
    return jsonify(data)
    



@app.route('/removeTagFromTagList',methods=['GET','POST'])
def removeTagFromTagList():
    
    

    tagListItems = request.form['tagListItems']
    tagListID =  request.form['tagListID']
    classIndex = str(tagListID.split('_')[1])
 
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()

    cursor.execute( u"UPDATE learning_map set tag = '%s' where index = %s;" % ( tagListItems, classIndex))

    conn.commit()
    conn.close()

    data = "del tag from DB"
    return jsonify(data)
    


@app.route('/addTagSampleTODB',methods=['GET','POST'])
def addTagSampleTODB():
    
    
    callDB  =callTactic()
    get3DDB =  callDB.get3DDB

    tagListItems = request.form['tagListItems']
    tagListID =  '\''+request.form['tagListID'] +'\''
 
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()

    cursor.execute( u"UPDATE tag_type set tag_list = '%s' where tag_class = %s;" % ( tagListItems, tagListID))

    conn.commit()
    conn.close()

    return jsonify(tagListItems)








@app.route('/getTagSampleFromDB',methods=['GET','POST'])
def getTagSampleFromDB():
    callDB  =callTactic()
    get3DDB =  callDB.get3DDB
    tagTypeDB = get3DDB.getRowDataFromTable('tag_type')

    tagTypeCount = len(tagTypeDB)
    
    tagSampeDict ={}
    

        
    for i in range(0,tagTypeCount):
        tagSampleList = tagTypeDB[i][2]
        tagTypeCode = tagTypeDB[i][0]
        tagClassDescription  = tagTypeDB[i][3]
        tagCssClass  = tagTypeDB[i][4]

        tagSampeDict.update({tagTypeDB[i][1]:{"tag_list":tagSampleList,
                                              "tag_type_code":tagTypeCode,
                                             "tag_class_description":tagClassDescription,
                                             "tag_type_code":tagTypeDB[i][0],
                                             "css_class":tagCssClass
                                             }})

  


    return jsonify(tagSampeDict)




@app.route('/writeFileDesctiption',methods=['GET','POST'])
def writeFileDesctiption():
    fileDescription = request.form['fileDesc']
    fileID =  request.form['fileID']
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    
    weireInDescription =  '\''+ fileDescription +'\''

    cursor.execute( u"UPDATE qc_db set description = '%s' where id = %s;" % ( fileDescription, fileID))

    conn.commit()
    conn.close()

    
    
    #return "writeFileDesctiption"
    return jsonify(fileDescription,fileID)







@app.route('/getClassCssFromDB',methods=['GET','POST'])
def getClassCssFromDB():
    
    callDB  =callTactic()
    get3DDB =  callDB.get3DDB
    tagTypeDB = get3DDB.getRowDataFromTable('tag_type')

    tagTypeCount = len(tagTypeDB)
    
    tagSampeDict ={}
    

    
    for i in range(0,tagTypeCount):
        tagSampleList = tagTypeDB[i][2]
        try:
            tagCount = len(tagSampleList.decode('utf8'))
        except:
            pass
    
    
    
    cssData = "dddd"
    return jsonify(cssData)







#personal learnning map

@app.route('/userLearning')
def userLearning():
    
    
    
    return render_template('userLearning.html ')
    






@app.route('/pixiTest')
def pixiTest():

    
   # return"pixi test"
    return render_template('pixiTest.html')


#currentImagesListPlay
## del select qc file in DB and s
@app.route('/imageList',methods=['GET','POST'])
def imageList():
    
    tempPlayImageList = request.form['imageList']
    playImageIndex = request.form['imageIndex']
    currentUser = request.form['currentUser']
   # print currentImagesList,type(currentImagesList)
    #currentImageIndex = request.form['currentImageIndex']
    name = '\"' + currentUser + '\"'
    
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
   # playImageList =tempPlayImageList.split(',')
   # weiteInPlayList = str(playImageList)
    inputData = "sfdsfdfd"
    cursor.execute( u"UPDATE user_db set images_list = '%s' where user_id ='%s';" % ( tempPlayImageList,currentUser))
    cursor.execute( u"UPDATE user_db set current_view_index = '%s' where user_id ='%s';" % ( playImageIndex,currentUser))

    conn.commit()
    conn.close()
    #print 'tempPlayImageList',tempPlayImageList
   # for i in playImageList:
   #     print "playList",i
    return jsonify(tempPlayImageList)
    
    #return "currentImagesListPlay" current_view_index
    
    
@app.route('/imageListRequest',methods=['GET','POST'])
def imageListRequest():
      
    currentUser = request.form['currentUser']

    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    name = '\"'+ currentUser + '\"'
    cursor.execute("SELECT * FROM user_db WHERE user_id = '%s'"%currentUser)
    rowData = cursor.fetchall()
    currentViewList = rowData[0][4]
    currentViewIndex = rowData[0][21]
    conn.commit()
    conn.close()
    userViewImagesList =  currentViewList[1:-1].split(',')
    print userViewImagesList[0]
    
    
    
    return jsonify(userViewImagesList,currentViewIndex)
   # return "currentImagesListPlay"

## del select qc file in DB and s
@app.route('/delFileItemInDB',methods=['GET','POST'])
def delFileItemInDB():
    currentFileID = request.form['currentFileID']

    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qc_db WHERE id = %s"%currentFileID)
    rowData = cursor.fetchone()
    fileType = rowData[10]
    cursor.execute("DELETE FROM qc_db WHERE id =%s"%currentFileID)
    conn.commit()
    conn.close()
   # print 'check code 0'
    if fileType == 'spine':
        
        jsonFileFullName =  rowData[1]
        jsonFileName = jsonFileFullName.split('/')[-1]
        fileLocation = jsonFileFullName.split(jsonFileName)[0]
        
        allFile = os.listdir(fileLocation)
        for i in allFile:
            fileName = fileLocation+i
            os.remove(fileName)
        #print 'check code 1'

    else:
        fileName =rowData[1] 
        iconFileName = rowData[16] 
        os.remove(fileName)
        os.remove(iconFileName)
        #print 'check code 2'



    
    return "delete Select Item From DB "

    

##login  ##檢查帳號密碼
@app.route('/loginMatch',methods=['GET','POST'])
def loginMatch():
    
    loginID = request.form['loginID']
    loginPS = request.form['loginPS']
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_db")
    rowData = cursor.fetchall()

    conn.commit()
    conn.close()
    #print rowData
    userData = filter(lambda x:x[2] == loginID,rowData)
    if userData[0][9] ==loginPS:
        state = True
    else:
        state = False

    
    return jsonify(state)  





##得到圖片大小
@app.route('/getImageRes',methods=['GET','POST'])
def getImageRes():
    
    fileLinkUrl = request.form['fileLinkUrl']
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qc_db")
    rowData = cursor.fetchall()
    fileData = filter(lambda x:x[21] == fileLinkUrl,rowData)
    conn.commit()
    conn.close()
    res = int(fileData[0][11].split(']___')[0].split('size[')[1].split(',')[0])
    windowWidth = 1800
    if res <= windowWidth:
        resRatio = str(res)+'px'
    else:
        resRatio = str(int((windowWidth/(float(res)))*100.0 )) +'%'
        
    
    return jsonify(resRatio)  





#######"取得目前執行的專案"
@app.route('/getProjectsWorkOn',methods=['GET','POST'])
def getProjectsWorkOn():
    
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games_db")
    rowData = cursor.fetchall()
    conn.commit()
    conn.close()    
    
    tempGamesData = filter(lambda x:x[4] == ".In Progress",rowData)
    
    gamesData = list((sorted(tempGamesData, key = lambda x: x[0])))

  
    
    
    return jsonify(gamesData)  










#####"專案管理頁面"

@app.route('/pm')
def proejctManager():
    
    
    #return "projects Manager"
    return render_template('projectManager.html ')
    




###取得tactic simpleslot/game game DB

@app.route('/get3DDBGameDB',methods=['GET','POST'])
def get3DDBGameDB():
    '''
    conn = psycopg2.connect(database='simpleslot', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM game")
    tempAllProjects = cursor.fetchall()
    
    
    allProjects = list(reversed(sorted(tempAllProjects, key = lambda x: int(x[7]))))
    inProgressProjects =filter(lambda x:x[12] =='.In Progress' ,allProjects)
    completedProjects =filter(lambda x:x[12] =='.Complete' ,allProjects)

    conn.commit()
    conn.close()    
    '''
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games_db")
    tempAllGamesInDB = cursor.fetchall()
    conn.commit()
    conn.close()    
    allProjects = list(reversed(sorted(tempAllGamesInDB, key = lambda x: int(x[1]))))
    inProgressProjects =filter(lambda x:x[4] =='.In Progress' ,allProjects)
    completedProjects =filter(lambda x:x[4] =='.Complete' ,allProjects)
    
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pc")
    pcDB = cursor.fetchall()
    conn.commit()
    conn.close()      
    
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_db")
    tempUserDB = cursor.fetchall()
    userDB = list((sorted(tempUserDB, key = lambda x: x[2])))
    conn.commit()
    conn.close()      
      
    
    

    return jsonify(inProgressProjects,completedProjects,allProjects,pcDB,userDB)




@app.route('/addNewProjInTactic',methods=['GET','POST'])
def addNewProjInTactic():

    tactic = runTactic()
    server=tactic.server
    tactic_server_ip= tactic.tactic_server_ip
    #print server
        
    server.set_server(tactic_server_ip)
    server.set_project("simpleslot")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)

    projectName = request.form['projectName']
    projectCNName = request.form['projectCNName']
    windowUserName = request.form['windowUserName']
    pcName = request.form['pcName']
    newProjectStartTime = (request.form['newProjectStartTime']).replace('/','-')
    newProjectEndTime = (request.form['newProjectEndTime']).replace('/','-')
    
    #print 
    search_type ='simpleslot/game'
    data ={
        'name': projectName,
        'name_chn':projectCNName,
        'project_status':'.In Progress',
        'project_coordinator': pcName,
        'brief_sd':newProjectStartTime,
        'brief_ed':newProjectEndTime
    }
    try:
        server.insert(search_type, data)
        errorMsg ="null"
    except Exception, e:
        errorMsg = str(e)   
    
    return jsonify(errorMsg)






#### get project/game, assets ,shots data from 3DDB 
@app.route('/getProjectDataWhenClickEditBtn',methods=['GET','POST'])
def getProjectDataWhenClickEditBtn():
    ### get project/games data from 3D_db
    projectName = request.form['projectName']
    
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games_db")
    allProjectsData = cursor.fetchall()
    selectGameDB = filter(lambda x:x[0] == projectName ,allProjectsData)
    conn.commit()
    conn.close()  
    
    ### get assets data from 3D_db
    conn2 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM assets")
    allAssetsData= cursor2.fetchall()
    selectAssetsDB = filter(lambda x:x[11] == projectName ,allAssetsData)
    conn2.commit()
    conn2.close()       
    

    ### get Shots data from 3D_db
    conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM shots")
    allShotsData= cursor3.fetchall()
    selectShotsDB = filter(lambda x:x[10] == projectName ,allShotsData)
    conn3.commit()
    conn3.close()       
    
    gameCode = "GAME"+'{:05d}'.format(selectGameDB[0][8])
    
    
    return jsonify(selectGameDB,selectAssetsDB,selectShotsDB,gameCode)












#### 同步專案 tactic <--> 3ddb
@app.route('/pm_syncProjectsBtn',methods=['GET','POST'])
def pm_syncProjectsBtn():
    
    projSyncMsg = "start"

    ### get all project data from tactic/games
    allGamesID = []  ### all ID in Tactic/game
    allGamesIDIn3DDB  = [] ### all Data in 3DDB/games_db
    #########
    allIdNotIn3DDB =[]  ###all id in Tactic/games but not in 3DDB/games_db
    allIDNotInTactic =[] ###all id in 3DDB/games_db not in tactic/games  
    
    
    ###----------------###
    conn = psycopg2.connect(database='simpleslot', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM game")
    tempAllGamesData = cursor.fetchall()
    allGamesData = list((sorted(tempAllGamesData, key = lambda x: x[7]))) #all assets data
    


    for i in range(0,len(allGamesData)):
        allGamesID.append(allGamesData[i][7])
    allGamesID = sorted(allGamesID)
    
    conn.commit()
    conn.close()       
    
    
    ### get all data from 3DDB/games_db
    
    conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM games_db")
    tempAllGamesIn3DDB = cursor3.fetchall()
    conn3.commit()
    conn3.close()  
    allGamesDataIn3DDB = list((sorted(tempAllGamesIn3DDB, key = lambda x: x[1])))
    allGamesDataIn3DDB = sorted(allGamesDataIn3DDB)
    allGamesIn3DDBCount = len(allGamesDataIn3DDB)
    
    for i in range(0,allGamesIn3DDBCount):
        allGamesIDIn3DDB.append(allGamesDataIn3DDB[i][8] )
    
    allGamesIDIn3DDB = sorted(allGamesIDIn3DDB)

        
    for i in allGamesID:
        if i not in allGamesIDIn3DDB:
            allIdNotIn3DDB.append(i)
        else:
            pass
        
    for i in allGamesIDIn3DDB:
        if i not in allGamesID:
            allIDNotInTactic.append(i)
        else:
            pass
    
    
    
    
    ##### delete project element in 3DDB/games_db but not in Tactic/game
    
    if len(allIDNotInTactic) == 0:
        pass
    else:
        for searchKey in allIDNotInTactic:
         
            conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
            cursor3 = conn3.cursor()
            cursor3.execute('DELETE FROM games_db WHERE index = %s'%searchKey)
            conn3.commit()
            conn3.close()
            
    ##### add project element into 3DDB/games_db
    
    if len(allIdNotIn3DDB) == 0:
        pass
    else:
        for i in allIdNotIn3DDB:
            conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
            cursor3 = conn3.cursor()    
            try:
                cursor3.execute("INSERT INTO games_db (index) VALUES(%s)"%i)
            except:
                pass
            conn3.commit()
            conn3.close()  
    
   ##### renew games_db(project) in 3DDB assets     
    conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor3 = conn3.cursor()  
    for i in allGamesID:
       # conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
        #cursor3 = conn3.cursor()  
        projectData = filter(lambda x:x[7] == i ,allGamesData)
        name = projectData[0][8]
        code = str(projectData[0][7])
        game_type_code = projectData[0][11]
        name_chn = projectData[0][10]
        project_status = projectData[0][12]
        pc = projectData[0][16]
        brief_sd = projectData[0][14]
        brief_ed = projectData[0][15]
        qc_dir ="e:/webServer/database/"+ name +"/qc"
        
        
        
        ####check and sync project icon
        iconDirSource = tacticProjectDBPath +"/"+ name +"/icon"
        iconFileNameSource = iconDirSource +"/"+ name +"_v001_icon.png"
        targetFileName = projectIconPath +"/"+ name +"_v001_icon.png"
        if os.path.isfile(iconFileNameSource) == True:
            try:
                #print iconFileNameSource,targetFileName
                copyfile(iconFileNameSource, targetFileName) 
                project_icon_url = "http://192.168.161.193:8080/database/projects/projectIcons/"+ name +"_v001_icon.png"
            except:
                pass
        else:
            
            project_icon_url = "http://192.168.161.193:8080/database/projects/projectIcons/no_image.png"
        
        
        try:
            cursor3.execute( "UPDATE games_db set name = '%s' where index = '%s';" % ( name, i))
            cursor3.execute( "UPDATE games_db set code = '%s' where index = '%s';" % ( code, i))
            cursor3.execute( "UPDATE games_db set game_type_code = '%s' where index = '%s';" % ( game_type_code, i))
            cursor3.execute( "UPDATE games_db set name_chn = '%s' where index = '%s';" % ( name_chn, i))
            cursor3.execute( "UPDATE games_db set project_status = '%s' where index = '%s';" % ( project_status, i))
            cursor3.execute( "UPDATE games_db set pc = '%s' where index = '%s';" % ( pc, i))
            cursor3.execute( "UPDATE games_db set brief_sd = '%s' where index = '%s';" % ( brief_sd, i))
            cursor3.execute( "UPDATE games_db set brief_ed = '%s' where index = '%s';" % ( brief_ed, i))
            cursor3.execute( "UPDATE games_db set project_icon_url = '%s' where index = '%s';" % ( project_icon_url, i))
            cursor3.execute( "UPDATE games_db set qc_dir = '%s' where index = '%s';" % ( qc_dir, i))


        except:
            pass
    conn3.commit()
    conn3.close()  
    
    projSyncMsg = "finished"
        
    return jsonify(allGamesID,allGamesIDIn3DDB,allIdNotIn3DDB,allIDNotInTactic,projSyncMsg)
    
   # return "pm_syncProjectsBtn"
    
    
#### 同步shot tactic <--> 3ddb


@app.route('/pm_syncShotsBtn',methods=['GET','POST'])
def pm_syncShotsBtn():

    shotSyncMsg ='start'
    conn = psycopg2.connect(database='simpleslot', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shot")

    tempAllShotsData = cursor.fetchall()#[-10:]
    allShotsData = list((sorted(tempAllShotsData, key = lambda x: x[8]))) #all assets data
    allIDs = []     ### All shots ID in tactic
    
    for i in range(0,len(allShotsData)):
        allIDs.append(allShotsData[i][8])  
        
    allIDs = sorted(allIDs) ## all shots ID in tactic
    allShotsInTacticCount = len(allShotsData)
            
    
    ### get games data in Tactic, will be define game_name and game_chn_name  into allGameData
    conn.commit()
    conn.close()    
    
    conn2 = psycopg2.connect(database='simpleslot', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM game")

    allGameData = cursor2.fetchall()
    conn2.commit()
    conn2.close()        
       
    ### Shots DB in 3D_db
    
    conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM shots")
   # print allIDs
    tempAllShotsIn3DDB = cursor3.fetchall()
    allShotsDataIn3DDB = list((sorted(tempAllShotsIn3DDB, key = lambda x: x[7])))
    allAssetsCount = len(allShotsDataIn3DDB)
    
    allShotsIDinDB = []     ### id in assets/3ddb
    
    for i in range(0,allAssetsCount):
        allShotsIDinDB.append(allShotsDataIn3DDB[i][7])
        
    allShotsIDnotInDB =[] ##### id not in assets/3ddb    
    
    for i in allIDs:
        if i in allShotsIDinDB:
            pass
        else:
            allShotsIDnotInDB.append(i)

    conn3.commit()
    conn3.close()     
    
    #### check id in 3DDB/shots but not in Tactic/shot
    allShotsDoNotInTactic = [] ##### id in 3DDB/shots but not in Tactic/shot
    
    for i in allShotsIDinDB:
        if i not in allIDs:
            allShotsDoNotInTactic.append(i)
    
    if len(allShotsDoNotInTactic) == 0:
        pass
    else:
        print ('allShotsDoNotInTactic',allShotsDoNotInTactic)
        for searchKey in allShotsDoNotInTactic:
            conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
            cursor3 = conn3.cursor()
            ### delete all shots element in 3DDB/shots ,not in tactic/shot
            try:
                cursor3.execute('DELETE FROM shots WHERE id = %s'%searchKey) 
            except:
                pass
            conn3.commit()
            conn3.close() 
    ### add new id in shots/3ddb ，check new assets item in Tactic
    if len(allShotsIDnotInDB) == 0:
        pass
    else:
        for i in allShotsIDnotInDB:
            conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
            cursor3 = conn3.cursor()    
            try:
                cursor3.execute("INSERT INTO shots (id) VALUES(%s)"%i)
            except:
                pass
            conn3.commit()
            conn3.close() 
    
    
    ### renew  data in 3DDB/shots
    conn4 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor4 = conn4.cursor()  
    for i in allIDs:

        projectData = filter(lambda x:x[8] == i ,allShotsData)
        game_code = projectData[0][10]
        try:
            projectDataMatchID = filter(lambda x:x[1] == game_code ,allGameData)[0]
            game_name = projectDataMatchID[8]
            game_name_chn = projectDataMatchID[10]
        except:
            game_name =''
            game_name_chn =''    
    
        code = projectData[0][1]
        description = projectData[0][2]

        s_status = projectData[0][4]
        pipeline_code = projectData[0][5]
        keywords = projectData[0][6]
        name = projectData[0][9]

        login = projectData[0][7]
        timestamp = projectData[0][3]  
        #print game_name,i,type(game_name),type(i)


        try:
          #  print i

            cursor4.execute( "UPDATE shots set game_name = '%s' where id = '%s';" % ( game_name, i))
            cursor4.execute( "UPDATE shots set code = '%s' where id = '%s';" % ( code, i))
            cursor4.execute( "UPDATE shots set timestamp = '%s' where id = '%s';" % ( timestamp, i))
            cursor4.execute( "UPDATE shots set s_status = '%s' where id = '%s';" % ( s_status, i))
            cursor4.execute( "UPDATE shots set pipeline_code = '%s' where id = '%s';" % ( pipeline_code, i))
            cursor4.execute( "UPDATE shots set name = '%s' where id = '%s';" % ( name, i))
            cursor4.execute( "UPDATE shots set game_code = '%s' where id = '%s';" % ( game_code, i))
            cursor4.execute( "UPDATE shots set login = '%s' where id = '%s';" % ( login, i))
            cursor4.execute( "UPDATE shots set description = '%s' where id = '%s';" % ( description, i))  ## description is not unicode
            cursor4.execute( "UPDATE shots set game_name_chn = '%s' where id = '%s';" % ( game_name_chn, i))
            cursor4.execute( "UPDATE shots set keywords = '%s' where id = '%s';" % ( keywords, i))
                 

        except:
        

            pass
        
    conn4.commit()
    conn4.close() 

    
    
    shotSyncMsg ='finished'

    return jsonify(allShotsIDnotInDB,shotSyncMsg)




#### assets tactic <--> 3ddb


@app.route('/pm_syncAssetsBtn',methods=['GET','POST'])
def pm_syncAssetsBtn():
    shotSyncMsg ='start'

    conn = psycopg2.connect(database='simpleslot', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assets")

    tempAllAssetsData = cursor.fetchall()#[-10:]
    allAssetsData = list((sorted(tempAllAssetsData, key = lambda x: x[8]))) #all assets data
    allIDs = [] ###id in assets/tactic
    for i in range(0,len(allAssetsData)):
        allIDs.append(allAssetsData[i][8])  
    allIDs = sorted(allIDs) ## all assets ID in tactic
        
    allAssetsCount = len(allAssetsData)
    conn.commit()
    conn.close()    
    
    conn2 = psycopg2.connect(database='simpleslot', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM game")

    allGameData = cursor2.fetchall()
    conn2.commit()
    conn2.close()        
    
    ### assets DB in 3D_db
    conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM assets")
    
   # print allIDs
    tempAllAssetsIn3DDB = cursor3.fetchall()
    conn3.commit()
    conn3.close() 
    allAssetsDataIn3DDB = list((sorted(tempAllAssetsIn3DDB, key = lambda x: x[12])))
    allAssetsCount = len(allAssetsDataIn3DDB)
    allIDinDB = [] ## id in assets/3ddb
    for i in range(0,allAssetsCount):
        allIDinDB.append(allAssetsDataIn3DDB[i][12])
        
    
    #### check id in 3DDB/assets which is NOT IN TACTIC
    allIDnotInTactic=[]  ##不在tactic中但是在3DDB/ASSETS中   
  
    for i in allIDinDB:
        if i not in allIDs:
            allIDnotInTactic.append(i)
    
    if len(allIDnotInTactic) == 0 :
        pass
    else:
        #print ('allIDnotInTactic',allIDnotInTactic)

        ####delete element in 3DDB/ASSET
        for searchKey in allIDnotInTactic:
            conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
            cursor3 = conn3.cursor()
            cursor3.execute('DELETE FROM assets WHERE id = %s'%searchKey)
            conn3.commit()
            conn3.close() 
            
            
        
        
    #print "allIDnotInTactic",allIDnotInTactic
        
        
        
    allIDnotInDB =[] ##### id not in assets/3ddb     
    for i in allIDs:
        if i in allIDinDB:
            pass
        else:
            allIDnotInDB.append(i)


    print 'allIDnotInDB',allIDnotInDB
    
    ### add new id in assets/3ddb ，check new assets item in Tactic
    if len(allIDnotInDB) ==0:
        pass
    else:
        for i in allIDnotInDB:
            conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
            cursor3 = conn3.cursor()    
            try:
                cursor3.execute("INSERT INTO assets (id) VALUES(%s)"%i)
            except:
                pass
            conn3.commit()
            conn3.close() 
    
    
    ## renew data in 3DDB assets
    
    conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor3 = conn3.cursor()     
    
    for i in allIDs:

        projectData = filter(lambda x:x[8] == i ,allAssetsData)
        game_code = projectData[0][10]
        try:
            projectDataMatchID = filter(lambda x:x[1] == game_code ,allGameData)[0]
            game_name = projectDataMatchID[8]
            game_name_chn = projectDataMatchID[10]
        except:
            game_name =''
            game_name_chn =''
        code = projectData[0][1]
        description = projectData[0][2]
        #iIn = '\"' + str(i) + '\"'
        #descriptionIn = '\"' + description + '\"'
        s_status = projectData[0][4]
        pipeline_code = projectData[0][5]
        keywords = projectData[0][6]
        name = projectData[0][9]
        asset_type_code = projectData[0][11]
        frames = projectData[0][12]
        login = projectData[0][7]
        timestamp = projectData[0][3]               


        try:

            cursor3.execute( u"UPDATE assets set game_name = '%s' where id = '%s';" % ( game_name, i))
            cursor3.execute( u"UPDATE assets set code = '%s' where id = '%s';" % ( code, i))
            cursor3.execute( u"UPDATE assets set timestamp = '%s' where id = '%s';" % ( timestamp, i))
            cursor3.execute( u"UPDATE assets set s_status = '%s' where id = '%s';" % ( s_status, i))
            cursor3.execute( u"UPDATE assets set pipeline_code = '%s' where id = '%s';" % ( pipeline_code, i))
            cursor3.execute( u"UPDATE assets set name = '%s' where id = '%s';" % ( name, i))
            cursor3.execute( u"UPDATE assets set game_code = '%s' where id = '%s';" % ( game_code, i))
            cursor3.execute( u"UPDATE assets set asset_type_code = '%s' where id = '%s';" % ( asset_type_code, i))
            cursor3.execute( u"UPDATE assets set frames = '%s' where id = '%s';" % ( frames, i))
            cursor3.execute( u"UPDATE assets set login = '%s' where id = '%s';" % ( login, i))
            cursor3.execute( "UPDATE assets set description = '%s' where id = '%s';" % ( description, i))  ## description is not unicode
            cursor3.execute( "UPDATE assets set game_name_chn = '%s' where id = '%s';" % ( game_name_chn, i))
            cursor3.execute( "UPDATE assets set keywords = '%s' where id = '%s';" % ( keywords, i))
                 

        except:
        

            pass
        
    conn3.commit()
    conn3.close() 

        
        
    ###delete asset within 3DDB/assets but not in tactic
    #conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    #cursor3 = conn3.cursor()
    #cursor3.execute("SELECT * FROM assets")
    #tempAllAssetsIn3DDB = cursor3.fetchall()
    
   # print len(allIDinDB)
   # print len(allIDs)
   # for i in range(0,allASsetsCount):
    shotSyncMsg ='finished'
   
    
    return jsonify(allGameData,shotSyncMsg)





@app.route('/storeModifyTo3DDB',methods=['GET','POST'])
def storeModifyTo3DDB():

    
    gameName = request.form['gameName']
    gameNameChn = request.form['gameNameChn']
    projectPM = request.form['projectPM']
    projectPC = request.form['projectPC']
    projectBriefSD = request.form['projectBriefSD']
    projectBriefED = request.form['projectBriefED']
    projectWorkingOn = request.form['projectWorkingOn']
    projectStatus = request.form['projectStatus']
    projectCode = request.form['projectCode']

    #### update 3DDB/games_db
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    try:
        cursor.execute( "UPDATE games_db set pm ='%s',pc='%s',brief_sd='%s',brief_ed='%s',workon_user='%s',project_status='%s' WHERE name ='%s'"%(projectPM,projectPC,projectBriefSD,projectBriefED,projectWorkingOn,projectStatus,gameName))
    except:
        pass
    conn.commit()
    conn.close() 

    
    #### update tactic/games
    tactic = runTactic()
    server=tactic.server
    tactic_server_ip= tactic.tactic_server_ip
    

    server.set_server(tactic_server_ip)
    server.set_project("simpleslot")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_type ='simpleslot/game'
    
    data ={
        'name': gameName,
        'name_chn':gameNameChn,
        'project_status':projectStatus,
        'login':projectWorkingOn,
        'timestamp':projectBriefSD,
        'brief_sd':projectBriefSD,
        'brief_ed':projectBriefED,
        'project_coordinator':projectPC,
        'pipeline_code':'simpleslot/game',
    }
    
    
    
    search_key = server.build_search_key(search_type, projectCode)


    try:
        server.update(search_key, data)

        errorMsg ="null"
    except Exception, e:
        errorMsg = str(e)  
    
    
    
    
    
    
    #data="aaaa"
    return jsonify(gameName,projectPM,projectPC,projectBriefSD,projectBriefED,projectWorkingOn,errorMsg)





### 新增加asset
@app.route('/submitAddNewAssetBtn',methods=['GET','POST'])
def submitAddNewAssetBtn():
    getData =  request.args#.get('assetEditorValue')
    assetName = getData['assetName']
    assetDesctiption = getData['assetDesctiption']
    assetClass = getData['assetClass']
    assetWorkUser = getData['assetWorkUser']
    assetTimeStart = (getData['assetTimeStart']).replace('/','-')
    assetTimeEnd = (getData['assetTimeEnd']).replace('/','-')
    gameName = getData['currentProjectSelecte']  
    
    
    conceptProcess =  getData['conceptProcess']    
    conceptTS =  getData['conceptTS']    
    conceptTD =  getData['conceptTD']    
    conceptWorkonUser =  getData['conceptWorkonUser']    
    conceptWorkonExtra =  getData['conceptWorkonExtra']    

    modelProcess =  getData['modelProcess']    
    modelTS =  getData['modelTS']    
    modelTD =  getData['modelTD']    
    modelWorkonUser =  getData['modelWorkonUser']    
    modelWorkonExtra =  getData['modelWorkonExtra']   
    
    textureProcess =  getData['textureProcess']    
    textureTS =  getData['textureTS']    
    textureTD =  getData['textureTD']    
    textureWorkonExtra =  getData['textureWorkonExtra']    
    textureWorkonUser =  getData['textureWorkonUser']    
   
    riggingProcess =  getData['riggingProcess']    
    riggingTS =  getData['riggingTS']    
    riggingTD =  getData['riggingTD']    
    riggingWorkonUser =  getData['riggingWorkonUser']    
    riggingWorkonExtra =  getData['riggingWorkonExtra']    
   
   

    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games_db")
   # print allIDs
    allGamesIn3DDB = cursor.fetchall()
    code = int(filter(lambda x:x[0] == gameName ,allGamesIn3DDB)[0][1])
    gameCode =  "GAME"+'{:05d}'.format(code)
    conn.commit()
    conn.close() 
    
    
    
    
    
    ###add new asset to tactic using tactic api
    tactic = runTactic()
    server=tactic.server
    tactic_server_ip= tactic.tactic_server_ip
    

    #print server
    if assetClass == "character" :
        assetType = "ASSET_TYPE00002"
    elif assetClass == "vehicle" :
        assetType = "ASSET_TYPE00003"
    elif assetClass == "set" :
        assetType = "ASSET_TYPE00004"
    elif assetClass == "prop" :
        assetType = "ASSET_TYPE00005"
    elif assetClass == "other" :
        assetType = "ASSET_TYPE00006"
    
    ### add asset to tactic


    server.set_server(tactic_server_ip)
    server.set_project("simpleslot")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_type ='simpleslot/assets'
    data ={
        'name': assetName,
        'description':assetDesctiption,
        'asset_type_code':assetType,
        'game_code':gameCode,
        'login':assetWorkUser,
        'timestamp':assetTimeStart
       # 'project_coordinator': pcName,
       # 'brief_sd':newProjectStartTime,
       # 'brief_ed':newProjectEndTime
    }
    try:
        server.insert(search_type, data)
        errorMsg ="null"
    except Exception, e:
        errorMsg = str(e)  
        
        


    ### get assetCode from tactic
    conn2 = psycopg2.connect(database='simpleslot', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM assets")
    allAssetsRowInTactic = cursor2.fetchall()
    
    try:
        searchData = filter(lambda x:x[9] == assetName ,allAssetsRowInTactic)[-1]
        assetCode = searchData[1]
        searchID =  searchData[8]
    except:
        assetCode = 'null'
        searchID = 'null'
    ### add asset task to tactic task
    ### add concept Task     
   
    dataConceptTask = {
        'assigned': conceptWorkonUser,
        'status': conceptProcess,
        'bid_start_date': conceptTS,
        'bid_end_date': conceptTD,
        'process': 'concept',
        'context': 'concept',
        'pipeline_code': '3d_task',
        'search_code': assetCode,     
        'description': conceptWorkonExtra,       
        'search_type': "simpleslot/assets?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot',     
      
    }
    
    server.set_server(tactic_server_ip)
    server.set_project("sthpw")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_type ='sthpw/task'
    try:
        server.insert(search_type, dataConceptTask)
        addConceptTaskErrorMsg ="null"
    except Exception, e:
        addConceptTaskErrorMsg = str(e)  
        
    ### add model Task     
    
    dataModeltTask = {
        'assigned': modelWorkonUser,
        'status': modelProcess,
        'bid_start_date': modelTS,
        'bid_end_date': modelTD,
        'process': 'model',
        'context': 'model',
        'pipeline_code': '3d_task',
        'search_code': assetCode,     
        'description': modelWorkonExtra,       
        'search_type': "simpleslot/assets?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot',     
      
    }
    
    server.set_server(tactic_server_ip)
    server.set_project("sthpw")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_type ='sthpw/task'
    try:
        server.insert(search_type, dataModeltTask)
        addModelTaskErrorMsg ="null"
    except Exception, e:
        addModelTaskErrorMsg = str(e)  
    
    ### add texture Task     
   
    dataTexturetTask = {
        'assigned': textureWorkonUser,
        'status': textureProcess,
        'bid_start_date': textureTS,
        'bid_end_date': textureTD,
        'process': 'texture',
        'context': 'texture',
        'pipeline_code': '3d_task',
        'search_code': assetCode,     
        'description': textureWorkonExtra,       
        'search_type': "simpleslot/assets?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot',     
      
    }
    
    server.set_server(tactic_server_ip)
    server.set_project("sthpw")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_type ='sthpw/task'
    try:
        server.insert(search_type, dataTexturetTask)
        addTextureTaskErrorMsg ="null"
    except Exception, e:
        addTextureTaskErrorMsg = str(e)  
        
    ### add rigging Task     
    dataRiggingTask = {
        'assigned': riggingWorkonUser,
        'status': riggingProcess,
        'bid_start_date': riggingTS,
        'bid_end_date': riggingTD,
        'process': 'rigging',
        'context': 'rigging',
        'pipeline_code': '3d_task',
        'search_code': assetCode,     
        'description': riggingWorkonExtra,       
        'search_type': "simpleslot/assets?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot',     
      
    }
    
    server.set_server(tactic_server_ip)
    server.set_project("sthpw")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_type ='sthpw/task'
    try:
        server.insert(search_type, dataRiggingTask)
        addRiggingTaskErrorMsg ="null"
    except Exception, e:
        addRiggingTaskErrorMsg = str(e)  
    
    exportErrorMsg =  addConceptTaskErrorMsg + "<"+"br"+">" + addModelTaskErrorMsg + "<"+"br"+">" + addTextureTaskErrorMsg  + "<"+"br"+">" + addRiggingTaskErrorMsg
    #print (assetEditorValue),type(assetEditorValue)
    
    ###### add task info to 3DDB assets
    
    conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM games_db")

    allGamesIn3DDB = cursor3.fetchall()
    getGameData = (filter(lambda x:x[1] == str(code) ,allGamesIn3DDB))[0]
    game_name = getGameData[0]
    game_name_chn = getGameData[3]
    conn3.commit()
    conn3.close() 
    #print 'game_name',game_name
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO assets (id,code,description,timestamp,game_code,asset_type_code,login,name,s_status,pipeline_code,keywords,frames,game_name,game_name_chn,brief_sd,brief_ed) VALUES(%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(searchID,assetCode,assetDesctiption,assetTimeStart,gameCode,assetType,assetWorkUser,assetName,'None','simpleslot/assets','None','None',game_name,game_name_chn.decode('utf8'),assetTimeStart,assetTimeEnd))

    conn.commit()
    conn.close() 

            
    export3DDB_conceptData = {
        'concept_user':conceptWorkonUser,
        'concept_status':conceptProcess,
        'concept_ts':conceptTS,
        'concept_te':conceptTD,
        'concept_desc':conceptWorkonExtra,  
    }
    
    export3DDB_modelData = {
        'model_user':modelWorkonUser,
        'model_status':modelProcess,
        'model_ts':modelTS,
        'model_te':modelTD,
        'model_desc':modelWorkonExtra,  
    }
  
    export3DDB_textureData = {
        'texture_user':textureWorkonUser,
        'texture_status':textureProcess,
        'texture_ts':textureTS,
        'texture_te':textureTD,
        'texture_desc':textureWorkonExtra,  
    }

    export3DDB_riggingData = {
        'rigging_user':riggingWorkonUser,
        'rigging_status':riggingProcess,
        'rigging_ts':riggingTS,
        'rigging_te':riggingTD,
        'rigging_desc':riggingWorkonExtra,  
    }   
    
    
    addTaskTo3DDBAssets(searchID,export3DDB_conceptData) 
    addTaskTo3DDBAssets(searchID,export3DDB_modelData) 
    addTaskTo3DDBAssets(searchID,export3DDB_textureData) 
    addTaskTo3DDBAssets(searchID,export3DDB_riggingData) 
  
    
    return jsonify(getData,data,assetName,errorMsg,exportErrorMsg,assetCode,dataConceptTask)
    
### 編輯asset
@app.route('/submitEditAssetBtn',methods=['GET','POST'])
def submitEditAssetBtn():
    getData =  request.args#.get('assetEditorValue')
    assetName = getData['assetName']
    assetCode = getData['assetCode']
    searchID = int(assetCode.split('ASSETS')[1])
    assetDesctiption = getData['assetDesctiption']
    assetClass = getData['assetClass']
    assetWorkUser = getData['assetWorkUser']
    assetTimeStart = (getData['assetTimeStart']).replace('/','-')
    assetTimeEnd = (getData['assetTimeEnd']).replace('/','-')
    gameName = getData['currentProjectSelecte']  
    
    
    conceptProcess =  getData['conceptProcess']    
    conceptTS =  getData['conceptTS']    
    conceptTD =  getData['conceptTD']    
    conceptWorkonUser =  getData['conceptWorkonUser']    
    conceptWorkonExtra =  getData['conceptWorkonExtra']    

    modelProcess =  getData['modelProcess']    
    modelTS =  getData['modelTS']    
    modelTD =  getData['modelTD']    
    modelWorkonUser =  getData['modelWorkonUser']    
    modelWorkonExtra =  getData['modelWorkonExtra']   
    
    textureProcess =  getData['textureProcess']    
    textureTS =  getData['textureTS']    
    textureTD =  getData['textureTD']    
    textureWorkonExtra =  getData['textureWorkonExtra']    
    textureWorkonUser =  getData['textureWorkonUser']    
   
    riggingProcess =  getData['riggingProcess']    
    riggingTS =  getData['riggingTS']    
    riggingTD =  getData['riggingTD']    
    riggingWorkonUser =  getData['riggingWorkonUser']    
    riggingWorkonExtra =  getData['riggingWorkonExtra']    
   
   

    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games_db")
   # print allIDs
    allGamesIn3DDB = cursor.fetchall()
    code = int(filter(lambda x:x[0] == gameName ,allGamesIn3DDB)[0][1])
    gameCode =  "GAME"+'{:05d}'.format(code)
    conn.commit()
    conn.close() 
    


    
    ###add new asset to tactic using tactic api
    tactic = runTactic()
    server=tactic.server
    tactic_server_ip= tactic.tactic_server_ip
    

    #print server
    if assetClass == "character" :
        assetType = "ASSET_TYPE00002"
    elif assetClass == "vehicle" :
        assetType = "ASSET_TYPE00003"
    elif assetClass == "set" :
        assetType = "ASSET_TYPE00004"
    elif assetClass == "prop" :
        assetType = "ASSET_TYPE00005"
    elif assetClass == "other" :
        assetType = "ASSET_TYPE00006"
    
    ### add asset to tactic


    server.set_server(tactic_server_ip)
    server.set_project("simpleslot")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_type ='simpleslot/assets'
   # code = 'vehicle001'
    
    
    data ={
        'name': assetName,
        'description':assetDesctiption,
        'asset_type_code':assetType,
        'game_code':gameCode,
        'login':assetWorkUser,
        'timestamp':assetTimeStart

    }

        


    search_key = server.build_search_key(search_type, assetCode)

    try:
        server.update(search_key, data)
        errorMsg ="null"
    except Exception, e:
        errorMsg = str(e)  
           
    
    conn4= psycopg2.connect(database='sthpw', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
    cursor4 = conn4.cursor()
    cursor4.execute("SELECT * FROM task")
    allTaskInTactic = cursor4.fetchall()
    allTaskData = filter(lambda x:x[32] == assetCode ,allTaskInTactic)
    concept_searchKey =  "TASK"+'{:08d}'.format(filter(lambda x:x[15] == 'concept' ,allTaskData)[0][0])

    model_searchKey =  "TASK"+'{:08d}'.format(filter(lambda x:x[15] == 'model' ,allTaskData)[0][0])
    texture_searchKey =  "TASK"+'{:08d}'.format(filter(lambda x:x[15] == 'texture' ,allTaskData)[0][0])
    rigging_searchKey =  "TASK"+'{:08d}'.format(filter(lambda x:x[15] == 'rigging' ,allTaskData)[0][0])



    conn4.commit()
    conn4.close()    
    
    
    dataConceptTask = {
        'assigned': conceptWorkonUser,
        'status': conceptProcess,
        'bid_start_date': conceptTS,
        'bid_end_date': conceptTD,
        'process': 'concept',
        'context': 'concept',
        'pipeline_code': '3d_task',
        'search_code': assetCode,     
        'description': conceptWorkonExtra,       
        'search_type': "simpleslot/assets?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot',     
      
    }

    server.set_server(tactic_server_ip)
    server.set_project("sthpw")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_typeC ='sthpw/task'
    
    search_key = server.build_search_key(search_typeC, concept_searchKey)

    try:
        server.update(search_key, dataConceptTask)
        addConceptTaskErrorMsg ="null"
    except Exception, e:
        addConceptTaskErrorMsg = str(e)  
        
    ### add model Task     
    
    dataModeltTask = {
        'assigned': modelWorkonUser,
        'status': modelProcess,
        'bid_start_date': modelTS,
        'bid_end_date': modelTD,
        'process': 'model',
        'context': 'model',
        'pipeline_code': '3d_task',
        'search_code': assetCode,     
        'description': modelWorkonExtra,       
        'search_type': "simpleslot/assets?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot',     
      
    }
    
    server.set_server(tactic_server_ip)
    server.set_project("sthpw")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_key = server.build_search_key(search_typeC, model_searchKey)

    try:
        server.update(search_key, dataModeltTask)
        addModelTaskErrorMsg ="null"
    except Exception, e:
        addModelTaskErrorMsg = str(e)  
    
    ### add texture Task     
   
    dataTexturetTask = {
        'assigned': textureWorkonUser,
        'status': textureProcess,
        'bid_start_date': textureTS,
        'bid_end_date': textureTD,
        'process': 'texture',
        'context': 'texture',
        'pipeline_code': '3d_task',
        'search_code': assetCode,     
        'description': textureWorkonExtra,       
        'search_type': "simpleslot/assets?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot',     
      
    }
    
    server.set_server(tactic_server_ip)
    server.set_project("sthpw")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    # 
    search_key = server.build_search_key(search_typeC, texture_searchKey)

    try:
        server.update(search_key, dataTexturetTask)
        addTextureTaskErrorMsg ="null"
    except Exception, e:
        addTextureTaskErrorMsg = str(e)  
        
    ### add rigging Task     
    dataRiggingTask = {
        'assigned': riggingWorkonUser,
        'status': riggingProcess,
        'bid_start_date': riggingTS,
        'bid_end_date': riggingTD,
        'process': 'rigging',
        'context': 'rigging',
        'pipeline_code': '3d_task',
        'search_code': assetCode,     
        'description': riggingWorkonExtra,       
        'search_type': "simpleslot/assets?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot',     
      
    }
    
    server.set_server(tactic_server_ip)
    server.set_project("sthpw")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_key = server.build_search_key(search_typeC, rigging_searchKey)
    try:
        server.update(search_key, dataRiggingTask)
        addRiggingTaskErrorMsg ="null"
    except Exception, e:
        addRiggingTaskErrorMsg = str(e)  
    
    exportErrorMsg =  addConceptTaskErrorMsg + "<"+"br"+">" + addModelTaskErrorMsg + "<"+"br"+">" + addTextureTaskErrorMsg  + "<"+"br"+">" + addRiggingTaskErrorMsg
    
    
    #print (assetEditorValue),type(assetEditorValue)
    
    ###### add task info to 3DDB assets
    
    conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM games_db")

    allGamesIn3DDB = cursor3.fetchall()
    getGameData = (filter(lambda x:x[1] == str(code) ,allGamesIn3DDB))[0]
    game_name = getGameData[0]
    game_name_chn = getGameData[3]
    conn3.commit()
    conn3.close() 
    #print 'game_name',game_name
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()


    cursor.execute("UPDATE assets SET name ='%s',description ='%s',timestamp ='%s',asset_type_code ='%s',login ='%s',brief_sd ='%s',brief_ed='%s',concept_user ='%s',concept_status ='%s',concept_ts='%s',concept_te='%s',concept_desc='%s',model_user ='%s',model_status='%s',model_ts='%s',model_te='%s',model_desc='%s',texture_user ='%s',texture_status='%s',texture_ts='%s',texture_te='%s',texture_desc='%s',rigging_user ='%s',rigging_status='%s',rigging_ts='%s',rigging_te='%s',rigging_desc='%s' WHERE id = %s"%(assetName,assetDesctiption,assetTimeStart,assetType,assetWorkUser,assetTimeStart,assetTimeEnd,conceptWorkonUser,conceptProcess,conceptTS,conceptTD,conceptWorkonExtra,modelWorkonUser,modelProcess,modelTS,modelTD,modelWorkonExtra,textureWorkonUser,textureProcess,textureTS,textureTD,textureWorkonExtra,riggingWorkonUser,riggingProcess,riggingTS,riggingTD,riggingWorkonExtra,searchID))

   
    conn.commit()
    conn.close() 

    return jsonify(getData,data,assetName,errorMsg,exportErrorMsg,assetCode,dataConceptTask,dataModeltTask,dataTexturetTask,dataRiggingTask,allTaskData,concept_searchKey,model_searchKey,texture_searchKey,rigging_searchKey)
    



    
def addTaskTo3DDBAssets(assetID,taskData):
    
    for key in taskData.keys():
        value = taskData[key]
       # print assetID,key,value
    
        conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
        cursor = conn.cursor()
        cursor.execute( u"UPDATE assets set %s = '%s' where id = %s" % ( key, value,assetID))

        conn.commit()
        conn.close() 

        
        
        
        
### 新增加shot





@app.route('/submitAddNewShotBtn',methods=['GET','POST'])
def submitAddNewShotBtn():   
    getData =  request.args
    shotName = getData['shotName']
    shotDesctiption = getData['shotDesctiption']
    shotWorkUser = getData['shotWorkUser']
    shotTimeStart = (getData['shotTimeStart']).replace('/','-')
    shotTimeEnd = (getData['shotTimeEnd']).replace('/','-')
    gameName = getData['currentProjectSelecte']  
    
    
    layoutTS =  getData['layoutTS']    
    layoutTD =  getData['layoutTD']    
    layoutProcess =  getData['layoutProcess']    
    layoutWorkonUser =  getData['layoutWorkonUser']    
    layoutWorkonExtra =  getData['layoutWorkonExtra']   
    
    animationTS =  getData['animationTS']    
    animationTD =  getData['animationTD']    
    animationProcess =  getData['animationProcess']    
    animationWorkonUser =  getData['animationWorkonUser']    
    animationWorkonExtra =  getData['animationWorkonExtra']    

    lightingTS =  getData['lightingTS']    
    lightingTD =  getData['lightingTD']    
    lightingProcess =  getData['lightingProcess']    
    lightingWorkonUser =  getData['lightingWorkonUser']    
    lightingWorkonExtra =  getData['lightingWorkonExtra']       

    effectsTS =  getData['effectsTS']    
    effectsTD =  getData['effectsTD']    
    effectsProcess =  getData['effectsProcess']    
    effectsWorkonUser =  getData['effectsWorkonUser']    
    effectsWorkonExtra =  getData['effectsWorkonExtra']       

    simulationTS =  getData['simulationTS']    
    simulationTD =  getData['simulationTD']    
    simulationProcess =  getData['simulationProcess']    
    simulationWorkonUser =  getData['simulationWorkonUser']    
    simulationWorkonExtra =  getData['simulationWorkonExtra']     

    compTS =  getData['compTS']    
    compTD =  getData['compTD']    
    compProcess =  getData['compProcess']    
    compWorkonUser =  getData['compWorkonUser']    
    compWorkonExtra =  getData['compWorkonExtra']     

    finalTS =  getData['finalTS']    
    finalTD =  getData['finalTD']    
    finalProcess =  getData['finalProcess']    
    finalWorkonUser =  getData['finalWorkonUser']    
    finalWorkonExtra =  getData['finalWorkonExtra']     
    

    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games_db")
   # print allIDs
    allGamesIn3DDB = cursor.fetchall()
    code = int(filter(lambda x:x[0] == gameName ,allGamesIn3DDB)[0][1])
    gameCode =  "GAME"+'{:05d}'.format(code)
    conn.commit()
    conn.close() 
    


    ###add new shot to tactic using tactic api  新增shot到tactic/shot
    tactic = runTactic()
    server=tactic.server
    tactic_server_ip= tactic.tactic_server_ip
    

    server.set_server(tactic_server_ip)
    server.set_project("simpleslot")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_type ='simpleslot/shot'
    data ={
        'name': shotName,
        'description':shotDesctiption,
        'game_code':gameCode,
        'login':shotWorkUser,
        'timestamp':shotTimeStart,
        'pipeline_code':'simpleslot/shot',
        

       # 'project_coordinator': pcName,
       # 'brief_sd':newProjectStartTime,
       # 'brief_ed':newProjectEndTime
    }
    try:
        server.insert(search_type, data)
        errorMsg ="null"
    except Exception, e:
        errorMsg = str(e)  


    ### get shotCode from tactic
    conn2 = psycopg2.connect(database='simpleslot', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM shot")
    allAssetsRowInTactic = cursor2.fetchall()
    
    try:
        searchData = filter(lambda x:x[9] == shotName ,allAssetsRowInTactic)[-1]
        shotCode = searchData[1]
        searchID =  searchData[8]
        
    except:
        shotCode = 'null'
        searchID = 'null'

    conn2.commit()
    conn2.close() 
    
    ### add asset task to tactic task
    ### add concept Task     
   
    dataLayoutTask = {
        'assigned': layoutWorkonUser,
        'status': layoutProcess,
        'bid_start_date': layoutTS,
        'bid_end_date': layoutTD,
        'process': 'layout',
        'context': 'layout',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description': layoutWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot'  
    }

    dataAnimationTask = {
        'assigned': animationWorkonUser,
        'status':  animationProcess,
        'bid_start_date':  animationTS,
        'bid_end_date':  animationTD,
        'process': 'animation',
        'context': 'animation',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description':  animationWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot'  
    }

    dataLightingTask = {
        'assigned': lightingWorkonUser,
        'status':  lightingProcess,
        'bid_start_date':  lightingTS,
        'bid_end_date':  lightingTD,
        'process': 'lighting',
        'context': 'lighting',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description':  lightingWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot'  
    }
    
    dataEffectsTask = {
        'assigned': effectsWorkonUser,
        'status':  effectsProcess,
        'bid_start_date':  effectsTS,
        'bid_end_date':  effectsTD,
        'process': 'effects',
        'context': 'effects',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description':  effectsWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot'  
    }
    
    dataSimulationTask = {
        'assigned': simulationWorkonUser,
        'status':  simulationProcess,
        'bid_start_date':  simulationTS,
        'bid_end_date':  simulationTD,
        'process': 'simulation',
        'context': 'simulation',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description':  simulationWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot'  
    }
        
    dataCompTask = {
        'assigned': compWorkonUser,
        'status':  compProcess,
        'bid_start_date':  compTS,
        'bid_end_date':  compTD,
        'process': 'comp',
        'context': 'comp',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description':  compWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot'  
    }
    
        
    dataFinalTask = {
        'assigned': finalWorkonUser,
        'status':  finalProcess,
        'bid_start_date':  finalTS,
        'bid_end_date':  finalTD,
        'process': 'final',
        'context': 'final',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description':  finalWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': searchID,     
        'project_code': 'simpleslot'  
    }    
    
    server.set_server(tactic_server_ip)
    server.set_project("sthpw")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_type ='sthpw/task'
    
    try:
        server.insert(search_type, dataLayoutTask)
        addLayoutTaskErrorMsg ="null"
    except Exception, e:
        addLayoutTaskErrorMsg = str(e)    
    
    try:
        server.insert(search_type, dataAnimationTask)
        addAnimationTaskErrorMsg ="null"
    except Exception, e:
        addAnimationTaskErrorMsg = str(e)  
 
    try:
        server.insert(search_type, dataLightingTask)
        addLightingTaskErrorMsg ="null"
    except Exception, e:
        addLightingTaskErrorMsg = str(e)  
               
    try:
        server.insert(search_type, dataEffectsTask)
        addEffectTaskErrorMsg ="null"
    except Exception, e:
        addEffectTaskErrorMsg = str(e)          
        
    try:
        server.insert(search_type, dataSimulationTask)
        addSimulationTaskErrorMsg ="null"
    except Exception, e:
        addSimulationTaskErrorMsg = str(e)        
     
    try:
        server.insert(search_type, dataCompTask)
        addCompTaskErrorMsg ="null"
    except Exception, e:
        addCompTaskErrorMsg = str(e)         
        
    try:
        server.insert(search_type, dataFinalTask)
        addFinalTaskErrorMsg ="null"
    except Exception, e:
        addFinalTaskErrorMsg = str(e)       
        
    exportErrorMsg =  addLayoutTaskErrorMsg + "<"+"br"+">" + addAnimationTaskErrorMsg + "<"+"br"+">" + addLightingTaskErrorMsg  + "<"+"br"+">" + addEffectTaskErrorMsg + "<"+"br"+">" + addSimulationTaskErrorMsg + "<"+"br"+">" + addCompTaskErrorMsg + "<"+"br"+">" + addFinalTaskErrorMsg

    ##### get game name
    conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM games_db")

    allGamesIn3DDB = cursor3.fetchall()
    getGameData = (filter(lambda x:x[1] == str(code) ,allGamesIn3DDB))[0]
    game_name = getGameData[0]
    game_name_chn = getGameData[3]
    conn3.commit()
    conn3.close() 
    
    #### add task info to 3DDB shots
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO shots (id,code,description,timestamp,game_code,login,name,s_status,pipeline_code,keywords,game_name,game_name_chn,brief_sd,brief_ed) VALUES(%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(searchID,shotCode,shotDesctiption,shotTimeStart,gameCode,shotWorkUser,shotName,'None','simpleslot/shot','None',game_name,game_name_chn.decode('utf8'),shotTimeStart,shotTimeEnd))
    conn.commit()

    conn.close() 
    
    export3DDB_layoutData = {
        'layout_user':layoutWorkonUser,
        'layout_status':layoutProcess,
        'layout_ts':layoutTS,
        'layout_te':layoutTD,
        'layout_desc':layoutWorkonExtra,  
    }
    
    export3DDB_animationData = {
        'animation_user':animationWorkonUser,
        'animation_status':animationProcess,
        'animation_ts':animationTS,
        'animation_te':animationTD,
        'animation_desc':animationWorkonExtra,  
    }
  
    export3DDB_lightingData = {
        'lighting_user':lightingWorkonUser,
        'lighting_status':lightingProcess,
        'lighting_ts':lightingTS,
        'lighting_te':lightingTD,
        'lighting_desc':lightingWorkonExtra,  
    }

    export3DDB_effectData = {
        'effect_user':effectsWorkonUser,
        'effect_status':effectsProcess,
        'effect_ts':effectsTS,
        'effect_te':effectsTD,
        'effect_desc':effectsWorkonExtra,  
    }   
 
    export3DDB_simulationData = {
        'simulation_user':simulationWorkonUser,
        'simulation_status':simulationProcess,
        'simulation_ts':simulationTS,
        'simulation_te':simulationTD,
        'simulation_desc':simulationWorkonExtra,  
    }   
    
    export3DDB_compData = {
        'comp_user':compWorkonUser,
        'comp_status':compProcess,
        'comp_ts':compTS,
        'comp_te':compTD,
        'comp_desc':compWorkonExtra,  
    }   
    
    export3DDB_finalData = {
        'final_user':finalWorkonUser,
        'final_status':finalProcess,
        'final_ts':finalTS,
        'final_te':finalTD,
        'final_desc':finalWorkonExtra,  
    }       
    
    addTaskTo3DDBShots(searchID,export3DDB_layoutData) 
    addTaskTo3DDBShots(searchID,export3DDB_animationData) 
    addTaskTo3DDBShots(searchID,export3DDB_lightingData) 
    addTaskTo3DDBShots(searchID,export3DDB_effectData) 
    addTaskTo3DDBShots(searchID,export3DDB_simulationData) 
    addTaskTo3DDBShots(searchID,export3DDB_compData) 
    addTaskTo3DDBShots(searchID,export3DDB_finalData) 
   
    return jsonify(getData,gameCode,shotName,errorMsg,exportErrorMsg)
    

    

    

@app.route('/submitEditShotBtn',methods=['GET','POST'])
def submitEditShotBtn():   
    getData =  request.args
    shotName = getData['shotName']
    shotCode = getData['shotCode']
    search_ID = int(shotCode.split('SHOT')[1])
    shotDesctiption = getData['shotDesctiption']
    shotWorkUser = getData['shotWorkUser']
    shotTimeStart = (getData['shotTimeStart']).replace('/','-')
    shotTimeEnd = (getData['shotTimeEnd']).replace('/','-')
    gameName = getData['currentProjectSelecte']  
    
    
    layoutTS =  getData['layoutTS']    
    layoutTD =  getData['layoutTD']    
    layoutProcess =  getData['layoutProcess']    
    layoutWorkonUser =  getData['layoutWorkonUser']    
    layoutWorkonExtra =  getData['layoutWorkonExtra']   
    
    animationTS =  getData['animationTS']    
    animationTD =  getData['animationTD']    
    animationProcess =  getData['animationProcess']    
    animationWorkonUser =  getData['animationWorkonUser']    
    animationWorkonExtra =  getData['animationWorkonExtra']    

    lightingTS =  getData['lightingTS']    
    lightingTD =  getData['lightingTD']    
    lightingProcess =  getData['lightingProcess']    
    lightingWorkonUser =  getData['lightingWorkonUser']    
    lightingWorkonExtra =  getData['lightingWorkonExtra']       

    effectsTS =  getData['effectsTS']    
    effectsTD =  getData['effectsTD']    
    effectsProcess =  getData['effectsProcess']    
    effectsWorkonUser =  getData['effectsWorkonUser']    
    effectsWorkonExtra =  getData['effectsWorkonExtra']       

    simulationTS =  getData['simulationTS']    
    simulationTD =  getData['simulationTD']    
    simulationProcess =  getData['simulationProcess']    
    simulationWorkonUser =  getData['simulationWorkonUser']    
    simulationWorkonExtra =  getData['simulationWorkonExtra']     

    compTS =  getData['compTS']    
    compTD =  getData['compTD']    
    compProcess =  getData['compProcess']    
    compWorkonUser =  getData['compWorkonUser']    
    compWorkonExtra =  getData['compWorkonExtra']     

    finalTS =  getData['finalTS']    
    finalTD =  getData['finalTD']    
    finalProcess =  getData['finalProcess']    
    finalWorkonUser =  getData['finalWorkonUser']    
    finalWorkonExtra =  getData['finalWorkonExtra']     
    
    
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games_db")
   # print allIDs
    allGamesIn3DDB = cursor.fetchall()
    code = int(filter(lambda x:x[0] == gameName ,allGamesIn3DDB)[0][1])
    gameCode =  "GAME"+'{:05d}'.format(code)
    conn.commit()
    conn.close() 
    


    ###add new shot to tactic using tactic api  新增shot到tactic/shot
    tactic = runTactic()
    server=tactic.server
    tactic_server_ip= tactic.tactic_server_ip
    

    server.set_server(tactic_server_ip)
    server.set_project("simpleslot")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_type ='simpleslot/shot'
    data ={
        'name': shotName,
        'description':shotDesctiption,
        'game_code':gameCode,
        'login':shotWorkUser,
        'timestamp':shotTimeStart,
        'pipeline_code':'simpleslot/shot',
        

       # 'project_coordinator': pcName,
       # 'brief_sd':newProjectStartTime,
       # 'brief_ed':newProjectEndTime
    }
    
    
    
    search_key = server.build_search_key(search_type, shotCode)


    try:
        server.update(search_key, data)

        errorMsg ="null"
    except Exception, e:
        errorMsg = str(e)  



    
        
    conn4= psycopg2.connect(database='sthpw', user= 'postgres', password= '', host= '192.168.163.60', port= '5432')
    cursor4 = conn4.cursor()
    cursor4.execute("SELECT * FROM task")
    allTaskInTactic = cursor4.fetchall()
    allTaskData = filter(lambda x:x[32] == shotCode ,allTaskInTactic)
    layout_searchKey =  "TASK"+'{:08d}'.format(filter(lambda x:x[15] == 'layout' ,allTaskData)[0][0])
    animation_searchKey =  "TASK"+'{:08d}'.format(filter(lambda x:x[15] == 'animation' ,allTaskData)[0][0])
    lighting_searchKey =  "TASK"+'{:08d}'.format(filter(lambda x:x[15] == 'lighting' ,allTaskData)[0][0])
    effects_searchKey =  "TASK"+'{:08d}'.format(filter(lambda x:x[15] == 'effects' ,allTaskData)[0][0])
    simulation_searchKey =  "TASK"+'{:08d}'.format(filter(lambda x:x[15] == 'simulation' ,allTaskData)[0][0])
    comp_searchKey =  "TASK"+'{:08d}'.format(filter(lambda x:x[15] == 'comp' ,allTaskData)[0][0])
    final_searchKey =  "TASK"+'{:08d}'.format(filter(lambda x:x[15] == 'final' ,allTaskData)[0][0])
    conn4.commit()
    conn4.close() 
    

    


    
    ### add asset task to tactic task
    server.set_server(tactic_server_ip)
    server.set_project("sthpw")
    ticket = server.get_ticket("julio", "1234")
    server.set_ticket(ticket)
    #print 
    search_typeT ='sthpw/task'

    


    dataLayoutTask = {
        'assigned': layoutWorkonUser,
        'status': layoutProcess,
        'bid_start_date': layoutTS,
        'bid_end_date': layoutTD,
        'process': 'layout',
        'context': 'layout',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description': layoutWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': search_ID,     
        'project_code': 'simpleslot'  
    }

    dataAnimationTask = {
        'assigned': animationWorkonUser,
        'status':  animationProcess,
        'bid_start_date':  animationTS,
        'bid_end_date':  animationTD,
        'process': 'animation',
        'context': 'animation',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description':  animationWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': search_ID,     
        'project_code': 'simpleslot'  
    }

    dataLightingTask = {
        'assigned': lightingWorkonUser,
        'status':  lightingProcess,
        'bid_start_date':  lightingTS,
        'bid_end_date':  lightingTD,
        'process': 'lighting',
        'context': 'lighting',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description':  lightingWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': search_ID,     
        'project_code': 'simpleslot'  
    }
    
    dataEffectsTask = {
        'assigned': effectsWorkonUser,
        'status':  effectsProcess,
        'bid_start_date':  effectsTS,
        'bid_end_date':  effectsTD,
        'process': 'effects',
        'context': 'effects',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description':  effectsWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': search_ID,     
        'project_code': 'simpleslot'  
    }
    
    dataSimulationTask = {
        'assigned': simulationWorkonUser,
        'status':  simulationProcess,
        'bid_start_date':  simulationTS,
        'bid_end_date':  simulationTD,
        'process': 'simulation',
        'context': 'simulation',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description':  simulationWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': search_ID,     
        'project_code': 'simpleslot'  
    }
        
    dataCompTask = {
        'assigned': compWorkonUser,
        'status':  compProcess,
        'bid_start_date':  compTS,
        'bid_end_date':  compTD,
        'process': 'comp',
        'context': 'comp',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description':  compWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': search_ID,     
        'project_code': 'simpleslot'  
    }
    
        
    dataFinalTask = {
        'assigned': finalWorkonUser,
        'status':  finalProcess,
        'bid_start_date':  finalTS,
        'bid_end_date':  finalTD,
        'process': 'final',
        'context': 'final',
        'pipeline_code': '3d_task',
        'search_code': shotCode,     
        'description':  finalWorkonExtra,       
        'search_type': "simpleslot/shot?project=simpleslot",     
        'search_id': search_ID,     
        'project_code': 'simpleslot'  
    }    


    
    
    
    search_key = server.build_search_key(search_typeT, layout_searchKey)
    try:
        server.update(search_key, dataLayoutTask)
        addLayoutTaskErrorMsg ="null"
    except Exception, e:
        addLayoutTaskErrorMsg = str(e) 
        
    search_key = server.build_search_key(search_typeT, animation_searchKey)
    try:
        server.update(search_key, dataAnimationTask)
        addAnimationTaskErrorMsg ="null"
    except Exception, e:
        addAnimationTaskErrorMsg = str(e)    
        
    search_key = server.build_search_key(search_typeT, lighting_searchKey)
    try:
        server.update(search_key, dataLightingTask)
        addLightingTaskErrorMsg ="null"
    except Exception, e:
        addLightingTaskErrorMsg = str(e)      
        
    search_key = server.build_search_key(search_typeT, effects_searchKey)
    try:
        server.update(search_key, dataEffectsTask)
        addEffectTaskErrorMsg ="null"
    except Exception, e:
        addEffectTaskErrorMsg = str(e)     
        
    
    search_key = server.build_search_key(search_typeT, simulation_searchKey)
    try:
        server.update(search_key, dataSimulationTask)
        addSimulationTaskErrorMsg ="null"
    except Exception, e:
        addSimulationTaskErrorMsg = str(e) 
   

    search_key = server.build_search_key(search_typeT, comp_searchKey)
    try:
        server.update(search_key, dataCompTask)
        addCompTaskErrorMsg ="null"
    except Exception, e:
        addCompTaskErrorMsg = str(e) 

    search_key = server.build_search_key(search_typeT, final_searchKey)
    try:
        server.update(search_key, dataFinalTask)
        addFinalTaskErrorMsg ="null"
    except Exception, e:
        addFinalTaskErrorMsg = str(e) 

    
   
    try:
        
        server.insert(search_type, dataAnimationTask)
        addAnimationTaskErrorMsg ="null"
    except Exception, e:
        addAnimationTaskErrorMsg = str(e)  
        
        

        
    exportErrorMsg =  addLayoutTaskErrorMsg + "<"+"br"+">" + addAnimationTaskErrorMsg + "<"+"br"+">" + addLightingTaskErrorMsg  + "<"+"br"+">" + addEffectTaskErrorMsg + "<"+"br"+">" + addSimulationTaskErrorMsg + "<"+"br"+">" + addCompTaskErrorMsg + "<"+"br"+">" + addFinalTaskErrorMsg
        
    ##### get game name
    conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM games_db")

    allGamesIn3DDB = cursor3.fetchall()
    getGameData = (filter(lambda x:x[1] == str(code) ,allGamesIn3DDB))[0]
    game_name = getGameData[0]
    game_name_chn = getGameData[3]
    conn3.commit()
    conn3.close() 
    
    #### add task info to 3DDB shots
    conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor = conn.cursor()

  
    
    cursor.execute("UPDATE shots SET name ='%s',description ='%s',timestamp ='%s',login='%s',brief_sd='%s',brief_ed='%s',layout_user='%s', layout_status='%s',layout_ts='%s',layout_te='%s',layout_desc='%s',animation_user='%s', animation_status='%s',animation_ts='%s',animation_te='%s',animation_desc='%s',lighting_user='%s',lighting_status='%s',lighting_ts='%s',lighting_te='%s',lighting_desc='%s',effect_user='%s',effect_status='%s',effect_ts='%s',effect_te='%s',effect_desc='%s',simulation_user='%s', simulation_status='%s',simulation_ts='%s',simulation_te='%s',simulation_desc='%s',comp_user='%s', comp_status='%s',comp_ts='%s',comp_te='%s',comp_desc='%s',final_user='%s', final_status='%s',final_ts='%s',final_te='%s',final_desc='%s' WHERE id = %s"%(shotName,shotDesctiption,shotTimeStart,shotWorkUser,shotTimeStart,shotTimeEnd,layoutWorkonUser,layoutProcess,layoutTS,layoutTD,layoutWorkonExtra,animationWorkonUser,animationProcess,animationTS,animationTD,animationWorkonExtra,lightingWorkonUser,lightingProcess,lightingTS,lightingTD,lightingWorkonExtra,effectsWorkonUser,effectsProcess,effectsTS,effectsTD,effectsWorkonExtra,simulationWorkonUser,simulationProcess,simulationTS,simulationTD,simulationWorkonExtra,compWorkonUser,compProcess,compTS,compTD,compWorkonExtra,finalWorkonUser,finalProcess,finalTS,finalTD,finalWorkonExtra,search_ID))
    
    
    conn.commit()

    conn.close() 
   
    return jsonify(data,shotCode,shotName,errorMsg,exportErrorMsg,allTaskData,layout_searchKey)
        
    
        
def addTaskTo3DDBShots(shotID,taskData):
    
    for key in taskData.keys():
        value = taskData[key]
       # print assetID,key,value
    
        conn = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
        cursor = conn.cursor()
        cursor.execute( u"UPDATE shots set %s = '%s' where id = %s" % ( key, value,shotID))

        conn.commit()
        conn.close() 
              
  

@app.route('/getSpecAssetDataFrom3DDB',methods=['GET','POST'])
def getSpecAssetDataFrom3DDB():
    
    assetID = int(request.form['assetID'])

    conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM assets")
    allAssetsIn3DDB = cursor3.fetchall()

    getAssetData = (filter(lambda x:x[12] == assetID ,allAssetsIn3DDB))[0]
    getGameCode = int(getAssetData[7].split('GAME')[1])
    cursor3.execute("SELECT * FROM games_db")
    allGamesIn3DDB = cursor3.fetchall()
    getGameData = (filter(lambda x:x[8] == getGameCode ,allGamesIn3DDB))[0]

    conn3.commit()
    conn3.close() 

    return jsonify(getAssetData,getGameData)

        
    
    
    
    
    
    
    
    
    
    
@app.route('/getSpecShotDataFrom3DDB',methods=['GET','POST'])
def getSpecShotDataFrom3DDB():   
    
    shotID = int(request.form['shotID'])
    conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM shots")
    allShotsIn3DDB = cursor3.fetchall()
    getShotData = (filter(lambda x:x[7] == shotID ,allShotsIn3DDB))[0]
    conn3.commit()
    conn3.close() 
   # getShotData ="aa"
    return jsonify(getShotData,shotID)
    
    
    
@app.route('/imageUpload',methods=['GET','POST'])
def imageUpload():   
    app.config['UPLOADED_PATH'] = uploadPath

    for f in request.files.getlist('file'):
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
       # print request.files.getlist('file')
    
    #return 
    
    return "finished"


@app.route('/defineImageUpload',methods=['GET','POST'])
def defineImageUpload():   
    errMsg= "專案 icon 上傳失敗"
    fileName = request.form['fileName']
    projectName = request.form['projectName']
    itemName = request.form['itemName']
    itemCode = int(request.form['itemCode'])

    uploadMode = request.form['uploadMode']
    sourceFileName = uploadPath +'/'+fileName
    currentTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    timeStamp = time.time()
    data = currentTime.split('_')[0]
    im = Image.open( sourceFileName )
    imageFormat = im.format
    imageSize = im.size
    imageMode = im.mode
    metaData ='size%s___format(%s)___mode(%s)'%(imageSize,imageFormat,imageMode)
    currentProjectPath = projectDBPath +'/' +projectName
    print uploadMode
    if uploadMode =="project":
        
        iconName = projectIconPath +'/' +projectName +'_v001_icon.png'
        proJectIconURL = "http://192.168.161.193:8080/database/projects/projectIcons"+'/' +projectName +'_v001_icon.png'

        width = 120
        ratio = float(width)/im.size[0]
        height = int(im.size[1]*ratio)
        createIcon = im.resize( (width, height), Image.BILINEAR )
        createIcon.save( iconName )  
        conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
        cursor3 = conn3.cursor()
        cursor3.execute( "UPDATE games_db set project_icon_url = '%s' where name = '%s';" % ( proJectIconURL, projectName))
        conn3.commit()
        conn3.close() 
        os.remove(sourceFileName)
        errMsg= "專案 icon 設定完成"
        
    elif uploadMode =="asset":
        currentAssetPath = currentProjectPath + '/assets' 
        cuttentAssetIconPath = currentAssetPath +'/icons'
        #print currentProjectPath,currentAssetPath,cuttentAssetIconPath
        try:
            os.makedirs(currentProjectPath)
        except:
            pass
        try:
            os.makedirs(currentAssetPath)
        except:
            pass
        try:
            os.makedirs(cuttentAssetIconPath)
        except:
            pass
        
        iconName = cuttentAssetIconPath +'/' +itemName +'_v001_icon.png'
        iconURL =  "http://192.168.161.193:8080/database/projects/" +projectName +'/assets/icons/'+itemName +'_v001_icon.png'
        
        width = 96
        ratio = float(width)/im.size[0]
        height = int(im.size[1]*ratio)
        createIcon = im.resize( (width, height), Image.BILINEAR )
        createIcon.save( iconName )  
        
        conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
        cursor3 = conn3.cursor()
        cursor3.execute( "UPDATE assets set icon_url = '%s' where name = '%s';" % ( iconURL, itemName))
        conn3.commit()
        conn3.close() 
        
        try:
            os.remove(sourceFileName)
        except:
            pass
        
        errMsg= "Asset icon 設定完成"
        
    elif uploadMode =="shot":
        currentShotPath = currentProjectPath + '/shots'
        cuttentShotIconPath = currentShotPath +'/icons'
        print currentShotPath,cuttentShotIconPath
        try:
            os.makedirs(currentProjectPath)
        except:
            pass
        try:
            os.makedirs(currentShotPath)
        except:
            pass
        try:
            os.makedirs(cuttentShotIconPath)
        except:
            pass
        
        iconName = cuttentShotIconPath +'/' +itemName +'_v001_icon.png'
        iconURL =  "http://192.168.161.193:8080/database/projects/" +projectName +'/shots/icons/'+itemName +'_v001_icon.png'
        
        width = 96
        ratio = float(width)/im.size[0]
        height = int(im.size[1]*ratio)
        createIcon = im.resize( (width, height), Image.BILINEAR )
        createIcon.save( iconName )  
        
        conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
        cursor3 = conn3.cursor()
        cursor3.execute( "UPDATE shots set icon_url = '%s' where name = '%s';" % ( iconURL, itemName))
        conn3.commit()
        conn3.close() 
        try:
            os.remove(sourceFileName)
        except:
            pass
        errMsg= "Shot icon 設定完成"        
 
        
    return jsonify(errMsg)
    
    

    
    
    
@app.route('/publishItemUpload',methods=['GET','POST'])
def publishItemUpload():    
    
    errMsg = "upload fail"
    app.config['UPLOADED_PATH'] = uploadPath

    for f in request.files.getlist('file'):
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    
    
    errMsg = "finished"

    
    return jsonify(errMsg)


    
@app.route('/definePublishItem',methods=['GET','POST'])
def definePublishItem():    
    
    errMsg = "upload fail"
    fileName = request.form['fileName']
    game_name = request.form['projectName']
    name = request.form['itemName']
    code = int(request.form['itemCode'])
    uploadMode = request.form['uploadMode']
    
    type = request.form['itemType']
    mode = request.form['itemMode']
    resx = int(request.form['itemResX'])
    resy = int(request.form['itemResY'])
    pivot_x = str(request.form['itemPivotX'])
    pivot_y = str(request.form['itemPivotY'])
    center_x = int(request.form['itemCenterX'])
    center_y = int(request.form['itemCenterY'])
    locate_x = int(request.form['itemLocateX'])
    locate_y = int(request.form['itemLocateY'])
    scale = str(request.form['itemScale'])
    opti = str(request.form['itemOpti'])
    init_vis = request.form['itemInitVis']
    z_depth = int(request.form['itemZdepth'])
    description = request.form['itemDesc']
    

    
    
    
    
    timestamp = datetime.datetime.now().strftime('%Y/%m/%d/%H/%M/%S/%f')
   # timestamp = time.time()
   # timestamp = currentTime.split('_')[0]
    currentProjectPath = projectDBPath +'/' +game_name
    currentProjectAssetDir = currentProjectPath +'/assets' 
    currentItemDir = currentProjectAssetDir + '/'+  name

    if uploadMode == "publishImage":
        
        file_url =  "http://192.168.161.193:8080/database/projects/" +game_name +'/assets/'+name +'/'+fileName

        sourceFileName = uploadPath +'/'+fileName
        
        file_dir = sourceFileName + '/'+ fileName
        

        conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
        cursor3 = conn3.cursor()
        cursor3.execute("SELECT * FROM publish")
        allPublishItem = cursor3.fetchall()
        getItemData= (filter(lambda x:int(x[21]) == int(code)  ,allPublishItem))#[0]
        conn3.commit()
        conn3.close()        
        
        
        if len(getItemData) > 0 :   ###do update publish
            inputData = (name,game_name,type,mode,resx,resy,pivot_x,pivot_y,center_x,center_y,locate_x,locate_y,scale,opti,init_vis,z_depth,description,file_url,file_dir,timestamp,code)
            conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
            cursor3 = conn3.cursor()
              
            cursor3.execute("UPDATE publish SET name = '%s' , game_name = '%s' , type = '%s', mode= '%s', resx = %s , resy = %s , pivot_x = '%s' , pivot_y = '%s' , center_x = %s , center_y = %s ,locate_x = %s , locate_y = %s , scale ='%s' , opti = '%s' , init_vis = '%s' , z_depth = %s , description = '%s' , file_url = '%s' , file_dir = '%s' , timestamp ='%s' WHERE code = %s "%(inputData))
            conn3.commit()
            conn3.close()        
            errMsg ="update %s with %s/%s finish"%(name,mode,type)
           # print'getItemData', getItemData
        
        else:
            conn3 = psycopg2.connect(database='3D_db', user= 'postgres', password= '', host= '192.168.161.193', port= '5432')
            cursor3 = conn3.cursor()
              
            inputData = (name,game_name,code,type,mode,resx,resy,pivot_x,pivot_y,center_x,center_y,locate_x,locate_y,scale,opti,init_vis,z_depth,description,file_url,file_dir,timestamp)
            cursor3.execute("INSERT INTO publish (name,game_name,code,type,mode,resx,resy,pivot_x,pivot_y,center_x,center_y,locate_x,locate_y,scale,opti,init_vis,z_depth,description,file_url,file_dir,timestamp) VALUES('%s','%s',%s,'%s','%s',%s,%s,'%s','%s',%s,%s,%s,%s,'%s','%s','%s',%s,'%s','%s','%s','%s')"%inputData)

            conn3.commit()
            conn3.close()        
            errMsg ="add %s with %s/%s finish"%(name,mode,type)
    
    return jsonify(errMsg,inputData,getItemData,allPublishItem,code)  
    #return jsonify(fileName)  
    
    
if __name__ == '__main__':
    app.run(host='192.168.161.193',debug=True,port = 80)