    #getDB = postgreSQLCall.callPostgre('3D_db','postgres','5j/u.42017','192.168.161.47','5432')  

    tempProjectInProcessRows= []
    tempProjectCompletedRows= []
    for i in range(0,len(tempProjectRows)):
        if tempProjectRows[i][12] == ".In Progress":
            tempProjectInProcessRows.append(tempProjectRows[i])
        elif tempProjectRows[i][12] == ".Complete":
            tempProjectCompletedRows.append(tempProjectRows[i])
    print "projectTypeCount",len(tempProjectInProcessRows),len(tempProjectCompletedRows)
    
    if request.method == 'POST':
        print "request.method",request.method
        projectRequest = request.form['projectState']
       # print "projectRequest",projectRequest
        listCount = request.form['listCount']
        if projectRequest == "process":
            print "projectRequest",projectRequest
           # print "tempProjectInProcessRows",len(tempProjectInProcessRows),tempProjectInProcessRows[-1]
            projectRows = tempProjectInProcessRows
           # return jsonify(projectRows)
        elif projectRequest == "complete":
            print "projectRequest",projectRequest
           # print "tempProjectCompletedRows",len(tempProjectCompletedRows),tempProjectCompletedRows[-1]
            projectRows = tempProjectCompletedRows
           # return jsonify(projectRows)
           # return jsonify(tempProjectCompletedRows)
        elif projectRequest == "recent":
            print "projectRequest",projectRequest
           # print "projectRows",len(projectRows[-50:]),projectRows[-1]
           # return jsonify(projectRows[-50:])
            projectRows = tempProjectRows[-50:]
           # return jsonify(projectRows)
