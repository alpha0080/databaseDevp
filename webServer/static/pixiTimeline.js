 
function pixiTimeline(pixiApp,itemName){
        var w = 200
        var h = 32
        var timelineScreenW = pixiApp.renderer.screen.width
        var timelineScreenH = pixiApp.renderer.screen.height
       // var timelinePanel = [pixiApp,itemName,w,h]
        
        var gap = 10
        
        var left = 2*h + 4*h + 2.5*w + 9*gap
        var top = 300
        var lineHeight = h + gap
        var style = {
            fontWeight: 'normal',
            fontSize: h/2,
            fontFamily: 'Arial',
            fill: '#ffffff',
            align: 'center',
          //  stroke: '#FFFFFF',
            strokeThickness: 1
            };
        
        //console.log('screenW',screenW,w)
        
        var itemLabel =  new PIXI.Container();// 個別物件最上層的 container

        var serNoLabel = new PIXI.Graphics();
        serNoLabel.name = 'serNoLabel_'+itemName
        serNoLabel.beginFill(0x555555);
        serNoLabel.lineStyle(1, 0xffffff, 1);
        serNoLabel.drawRoundedRect(0,0,2*h,h,5)
        serNoLabel.endFill();
        serNoLabel.x=gap
        serNoLabel.y= top + 0//timelineScreenH/2 -h/2
        serNoLabel.zOrder = 200
        
        var serNoText = new PIXI.Text('no.',style);
        serNoText.x = h +gap //timelineScreenW/2
        serNoText.y =top + 0.5*h// timelineScreenH/2
        serNoText.zOrder = 300
        serNoText.anchor.set(0.5);
         
        
        //顯示的check
        var visCheck = new PIXI.Graphics();
        visCheck.name = "visCheck_"+ itemName
        visCheck.lineStyle(1,0xffffff,1);
        visCheck.beginFill(0xaaFFaa, 1);
        visCheck.drawRoundedRect(0,0,h,h,5)
        visCheck.endFill(); 
        visCheck.x =  2*h + 2*gap//timelineScreenW/2 - w/2 -4*h - 3*gap// -h
        visCheck.y =top+ 0// timelineScreenH/2 -h/2
        
        // 鎖定的check
        var dragCheck = new PIXI.Graphics();
        dragCheck.name = "dragCheck_"+ itemName

        dragCheck.lineStyle(1,0xffffff,1);
        dragCheck.beginFill(0x555555, 1);
        dragCheck.drawRoundedRect(0,0,h,h,5)
        dragCheck.endFill(); 
        dragCheck.x =  2*h + h + 3*gap//timelineScreenW/2 - w/2 -3*h -2*gap
        dragCheck.y =  top+0//timelineScreenH/2 -h/2
             
 
        // 獨立顯示的check
        var soloVisCheck = new PIXI.Graphics();
        soloVisCheck.name = "soloVisCheck_"+ itemName

        soloVisCheck.lineStyle(1,0xffffff,1);
        soloVisCheck.beginFill(0xff5555, 0.2);
        soloVisCheck.drawRoundedRect(0,0,h,h,5)
        soloVisCheck.endFill(); 
        soloVisCheck.x =   2*h + 2*h + 4*gap//timelineScreenW/2 - w/2 -2*h -gap 
        soloVisCheck.y = top+ 0//timelineScreenH/2 -h/2
             
         // 展開的的check
        var extTimelineCheck = new PIXI.Graphics();
        extTimelineCheck.name = "extTimelineCheck_"+ itemName

        extTimelineCheck.lineStyle(1,0xffffff,1);
        extTimelineCheck.beginFill(0xff5555, 0.6);
        extTimelineCheck.moveTo(0,0)
        extTimelineCheck.lineTo(0, h);
        extTimelineCheck.lineTo(0.5774*h,h/2);
        extTimelineCheck.lineTo(0, 0);


        extTimelineCheck.endFill(); 
        extTimelineCheck.x =  2*h + 3*h + 5*gap//timelineScreenW/2 - w/2 -h 
        extTimelineCheck.y =  top+0//timelineScreenH/2 -h/2
                    
        
        
        
        var itemNameLabel = new PIXI.Graphics();
        itemNameLabel.name = 'itemNameLabel_'+itemName
        itemNameLabel.beginFill(0x555555);
        itemNameLabel.lineStyle(1, 0xffffff, 1);
        itemNameLabel.drawRoundedRect(0,0,w,h,5)
        itemNameLabel.endFill();
        itemNameLabel.x= 2*h + 4*h + 6*gap //timelineScreenW/2 -w/2
        itemNameLabel.y= top+0//timelineScreenH/2 -h/2
        itemNameLabel.zOrder = 200
        
        var itemNameText = new PIXI.Text(itemName,style);
        itemNameText.x = 2*h + 4*h + 6*gap +w/2//timelineScreenW/2
        itemNameText.y =top+0.5*h// timelineScreenH/2
        itemNameText.zOrder = 300
        itemNameText.anchor.set(0.5);
        
        var maskLabel = new PIXI.Graphics();
        maskLabel.name = 'maskLabel'+itemName
        maskLabel.beginFill(0x222222);
        maskLabel.lineStyle(1, 0xffffff, 1);
        maskLabel.drawRoundedRect(0,0,w,h,5)
        maskLabel.endFill();
        maskLabel.x= 2*h + 4*h + w + 7*gap //timelineScreenW/2 + w/2 +gap
        maskLabel.y= top+0//timelineScreenH/2 -h/2
        maskLabel.zOrder = 200
        
        var maskText = new PIXI.Text('maskName',style);
        maskText.x = 2*h + 4*h + 1.5*w + 7*gap //timelineScreenW/2 + w +gap
        maskText.y = top+0.5*h//timelineScreenH/2
        maskText.zOrder = 300
        maskText.anchor.set(0.5);
        
        var blendMode = new PIXI.Graphics();
        blendMode.name = 'maskLabel'+itemName
        blendMode.beginFill(0x222222);
        blendMode.lineStyle(1, 0xffffff, 1);
        blendMode.drawRoundedRect(0,0,w/2,h,5)
        blendMode.endFill();
        blendMode.x= 2*h + 4*h + 2*w + 8*gap //timelineScreenW/2 + 1.5*w +2*gap
        blendMode.y= top+0//timelineScreenH/2 -h/2
        blendMode.zOrder = 200
              
        
        
        var blendText = new PIXI.Text('blend',style);
        blendText.x =  2*h + 4*h + 2.25*w + 8*gap //timelineScreenW/2 + 1.75*w +20
        blendText.y = top+0.5*h//timelineScreenH/2
        blendText.zOrder = 300
        blendText.anchor.set(0.5);
        
        
        // timeline 的底部
        var timelineBGLabel = new PIXI.Graphics();
        var timeLineW =timelineScreenW - (2*h + 4*h + 3*w)
        console.log('timeLineW',timeLineW)
        timelineBGLabel.name = 'maskLabel'+itemName
        timelineBGLabel.beginFill(0x222222);
        timelineBGLabel.lineStyle(1, 0xffffff, 1);
        timelineBGLabel.drawRoundedRect(0,0,timeLineW,h,5)
        timelineBGLabel.endFill();
        timelineBGLabel.x=left// 2*h + 4*h + 2.5*w + 9*gap //timelineScreenW/2 + 2*w +30
        timelineBGLabel.y=top+0// 0//timelineScreenH/2 -h/2
        timelineBGLabel.zOrder = 200
        
        
        // timeline 的指示條
        var timelineClipLabel = new PIXI.Graphics();
        var timeLineClipW = timelineScreenW -2*h -2.5*w - 8*10
        timelineClipLabel.name = 'maskClipLabel'+itemName
        timelineClipLabel.beginFill(0xffaaaa,0.5);
        timelineClipLabel.lineStyle(1, 0xffaaaa, 1);
        timelineClipLabel.drawRoundedRect(0,0,timeLineW,h,5)
        timelineClipLabel.endFill();
        timelineClipLabel.x= left//2*h + 4*h + 2.5*w + 9*gap//timelineScreenW/2 + 2*w +30
        timelineClipLabel.y= top+0// 0//timelineScreenH/2 -h/2
        timelineClipLabel.zOrder = 200
        
    //展開後的 position
        var positionContainer = new PIXI.Container();
        // 前一格
        var prewPFrameCheck = new PIXI.Graphics();
        prewPFrameCheck.name = "prewPFrameCheck_"+ itemName

        prewPFrameCheck.lineStyle(1,0xffffff,1);
        prewPFrameCheck.beginFill(0x555555, 0.6);
        prewPFrameCheck.moveTo(0.5774*h,0)
        prewPFrameCheck.lineTo(0.5774*h, h);
        prewPFrameCheck.lineTo(0,h/2);
        prewPFrameCheck.lineTo(0.5774*h,0);


        prewPFrameCheck.endFill(); 
        prewPFrameCheck.x =  2*h + 4*h + 6*gap//timelineScreenW/2 - w/2 -h 
        prewPFrameCheck.y =  top+lineHeight//h + gap//timelineScreenH/2 -h/2
                    
        
        
        
        //設key的check
        var setPKey = new PIXI.Graphics();
        setPKey.name = "setPKey_"+ itemName
        setPKey.lineStyle(1,0xffffff,1);
        setPKey.beginFill(0x555555, 0.3);
        setPKey.drawCircle(0.5*h,0.5*h,0.4*h)//(0,0,h,h,0.5*h)
        setPKey.endFill(); 
        setPKey.x =  2*h + 5*h + 6*gap//timelineScreenW/2 - w/2 -4*h - 3*gap// -h
        setPKey.y = top +lineHeight//h +gap// timelineScreenH/2 -h/2
        
        
      // 下一格
        var nextPFrameCheck = new PIXI.Graphics();
        nextPFrameCheck.name = "nextPFrameCheck_"+ itemName

        nextPFrameCheck.lineStyle(1,0xffffff,1);
        nextPFrameCheck.beginFill(0x555555, 0.6);
        nextPFrameCheck.moveTo(0,0)
        nextPFrameCheck.lineTo(0, h);
        nextPFrameCheck.lineTo(0.5774*h,h/2);
        nextPFrameCheck.lineTo(0,0);


        nextPFrameCheck.endFill(); 
        nextPFrameCheck.x =  2*h + 6*h + 7*gap//timelineScreenW/2 - w/2 -h 
        nextPFrameCheck.y =  top+lineHeight//h + gap//timelineScreenH/2 -h/2
                      
        
        
        
        var positionLabel = new PIXI.Graphics();
        positionLabel.name = 'positionLabel_'+itemName
        positionLabel.beginFill(0x555555);
        positionLabel.lineStyle(1, 0xffffff, 1);
        positionLabel.drawRoundedRect(0,0,w,h,5)
        positionLabel.endFill();
        positionLabel.x= 2*h + 6*h + 10*gap //timelineScreenW/2 -w/2
        positionLabel.y=top+lineHeight// h + gap//timelineScreenH/2 -h/2
        positionLabel.zOrder = 200
        
        var positionText = new PIXI.Text('position',style);
        positionText.x = 2*h + 7*h + 7*gap +w/2//timelineScreenW/2
        positionText.y = top+lineHeight +0.5*h//0.5*h + 1*h + gap// timelineScreenH/2
        positionText.zOrder = 300
        positionText.anchor.set(0.5);
 
        var positionX_ValueLabel = new PIXI.Graphics();
        positionX_ValueLabel.name = 'positionX_ValueLabel_'+itemName
        positionX_ValueLabel.beginFill(0x222222);
        positionX_ValueLabel.lineStyle(1, 0xffffff, 1);
        positionX_ValueLabel.drawRoundedRect(0,0,w/2,h,5)
        positionX_ValueLabel.endFill();
        positionX_ValueLabel.x= 2*h + 4*h + 1.5*w + 7*gap//timelineScreenW/2 -w/2
        positionX_ValueLabel.y=top+lineHeight// h + gap//timelineScreenH/2 -h/2
        positionX_ValueLabel.zOrder = 200
        
        var x_Text = new PIXI.Text('x...',style);
        x_Text.x =2*h + 4*h + 1.75*w + 7*gap//timelineScreenW/2
        x_Text.y = top+0.5*h +lineHeight// 1*h + gap// timelineScreenH/2
        x_Text.zOrder = 300
        x_Text.anchor.set(0.5);    
        
        var positionY_ValueLabel = new PIXI.Graphics();
        positionY_ValueLabel.name = 'positionY_ValueLabel_'+itemName
        positionY_ValueLabel.beginFill(0x222222);
        positionY_ValueLabel.lineStyle(1, 0xffffff, 1);
        positionY_ValueLabel.drawRoundedRect(0,0,w/2,h,5)
        positionY_ValueLabel.endFill();
        positionY_ValueLabel.x= 2*h + 4*h + 2*w + 8*gap//timelineScreenW/2 -w/2
        positionY_ValueLabel.y= top+lineHeight //h + gap//timelineScreenH/2 -h/2
        positionY_ValueLabel.zOrder = 200
        
        var y_Text = new PIXI.Text('y...',style);
        y_Text.x = 2*h + 4*h + 2.25*w + 9*gap//timelineScreenW/2
        y_Text.y = 0.5*h + top+lineHeight//1*h + gap// timelineScreenH/2
        y_Text.zOrder = 300
        y_Text.anchor.set(0.5); 
        
        // position value timeline 的底部
        var positionTimelineLabel = new PIXI.Graphics();
        //var timeLineW = timelineScreenW - (2*h + 4*h + 3*w)// + 8*gap
        positionTimelineLabel.name = 'positionTimelineLabel_'+itemName
        positionTimelineLabel.beginFill(0x222222);
        positionTimelineLabel.lineStyle(1, 0xffffff, 1);
        positionTimelineLabel.drawRoundedRect(0,0,timeLineW,h,5)
        positionTimelineLabel.endFill();
        positionTimelineLabel.x= left//2*h + 4*h + 2.5*w + 9*gap //timelineScreenW/2 + 2*w +30
        positionTimelineLabel.y= top+lineHeight//h+gap//timelineScreenH/2 -h/2
        positionTimelineLabel.zOrder = 200
        
        positionContainer.addChild(prewPFrameCheck)
        positionContainer.addChild(setPKey)
        positionContainer.addChild(nextPFrameCheck)
        positionContainer.addChild(positionLabel)
        positionContainer.addChild(positionText)
        positionContainer.addChild(positionX_ValueLabel)
        positionContainer.addChild(x_Text)
        positionContainer.addChild(positionY_ValueLabel)
        positionContainer.addChild(y_Text)
        positionContainer.addChild(positionTimelineLabel)

   //展開後的 scale
        
        // 前一格
        var scaleContainer = new PIXI.Container();

        var prewSFrameCheck = new PIXI.Graphics();

        prewSFrameCheck.name = "prewSFrameCheck_"+ itemName

        prewSFrameCheck.lineStyle(1,0xffffff,1);
        prewSFrameCheck.beginFill(0x555555, 0.6);
        prewSFrameCheck.moveTo(0.5774*h,0)
        prewSFrameCheck.lineTo(0.5774*h, h);
        prewSFrameCheck.lineTo(0,h/2);
        prewSFrameCheck.lineTo(0.5774*h,0);


        prewSFrameCheck.endFill(); 
        prewSFrameCheck.x =  2*h + 4*h + 6*gap//timelineScreenW/2 - w/2 -h 
        prewSFrameCheck.y = top+ 2*lineHeight// 2*h + 2*gap//timelineScreenH/2 -h/2
                    
        
        
        
        //設key的check
        var setSKey = new PIXI.Graphics();
        setSKey.name = "setSKey_"+ itemName
        setSKey.lineStyle(1,0xffffff,1);
        setSKey.beginFill(0x555555, 0.3);
        setSKey.drawCircle(0.5*h,0.5*h,0.4*h)//(0,0,h,h,0.5*h)
        setSKey.endFill(); 
        setSKey.x =  2*h + 5*h + 6*gap//timelineScreenW/2 - w/2 -4*h - 3*gap// -h
        setSKey.y =top+ 2*lineHeight//2*h +2*gap// timelineScreenH/2 -h/2
        
        
      // 下一格
        var nextSFrameCheck = new PIXI.Graphics();
        nextSFrameCheck.name = "nextSFrameCheck_"+ itemName

        nextSFrameCheck.lineStyle(1,0xffffff,1);
        nextSFrameCheck.beginFill(0x555555, 0.6);
        nextSFrameCheck.moveTo(0,0)
        nextSFrameCheck.lineTo(0, h);
        nextSFrameCheck.lineTo(0.5774*h,h/2);
        nextSFrameCheck.lineTo(0,0);


        nextSFrameCheck.endFill(); 
        nextSFrameCheck.x =  2*h + 6*h + 7*gap//timelineScreenW/2 - w/2 -h 
        nextSFrameCheck.y =  top+ 2*lineHeight//2*h + 2*gap//timelineScreenH/2 -h/2
                      
        
        
        
        var scaleLabel = new PIXI.Graphics();
        scaleLabel.name = 'scaleLabel'+itemName
        scaleLabel.beginFill(0x555555);
        scaleLabel.lineStyle(1, 0xffffff, 1);
        scaleLabel.drawRoundedRect(0,0,w,h,5)
        scaleLabel.endFill();
        scaleLabel.x= 2*h + 6*h + 10*gap //timelineScreenW/2 -w/2 
        
        scaleLabel.y= top+ 2*lineHeight//2*h + 2*gap//timelineScreenH/2 -h/2
        scaleLabel.zOrder = 200
        
        var scaleText = new PIXI.Text('scale',style);
        scaleText.x = 2*h + 7*h + 7*gap +w/2//timelineScreenW/2  2*h + 7*h + 7*gap +w/2
        scaleText.y = 0.5*h +top+ 2*lineHeight//+ 2*h + 2*gap// timelineScreenH/2
        scaleText.zOrder = 300
        scaleText.anchor.set(0.5);
 
        var scaleX_ValueLabel = new PIXI.Graphics();
        scaleX_ValueLabel.name = 'scaleX_ValueLabel_'+itemName
        scaleX_ValueLabel.beginFill(0x222222);
        scaleX_ValueLabel.lineStyle(1, 0xffffff, 1);
        scaleX_ValueLabel.drawRoundedRect(0,0,w/2,h,5)
        scaleX_ValueLabel.endFill();
        scaleX_ValueLabel.x= 2*h + 4*h + 1.5*w + 7*gap//timelineScreenW/2 -w/2
        scaleX_ValueLabel.y=top+ 2*lineHeight// 2*h + 2*gap//timelineScreenH/2 -h/2
        scaleX_ValueLabel.zOrder = 200
        
        var sx_Text = new PIXI.Text('sx...',style);
        sx_Text.x =2*h + 4*h + 1.75*w + 7*gap//timelineScreenW/2
        sx_Text.y = 0.5*h + top+ 2*lineHeight//2*h + 2*gap// timelineScreenH/2
        sx_Text.zOrder = 300
        sx_Text.anchor.set(0.5);    
        
        var scaleY_ValueLabel = new PIXI.Graphics();
        scaleY_ValueLabel.name = 'scaleY_ValueLabel_'+itemName
        scaleY_ValueLabel.beginFill(0x222222);
        scaleY_ValueLabel.lineStyle(1, 0xffffff, 1);
        scaleY_ValueLabel.drawRoundedRect(0,0,w/2,h,5)
        scaleY_ValueLabel.endFill();
        scaleY_ValueLabel.x= 2*h + 4*h + 2*w + 8*gap//timelineScreenW/2 -w/2
        scaleY_ValueLabel.y= top+ 2*lineHeight//2*h + 2*gap//timelineScreenH/2 -h/2
        scaleY_ValueLabel.zOrder = 200
        
        var sy_Text = new PIXI.Text('sy...',style);
        sy_Text.x = 2*h + 4*h + 2.25*w + 9*gap//timelineScreenW/2
        sy_Text.y = 0.5*h +top+ 2*lineHeight// 2*h + 2*gap// timelineScreenH/2
        sy_Text.zOrder = 300
        sy_Text.anchor.set(0.5); 
        
        // position value timeline 的底部
        var scaleTimelineLabel = new PIXI.Graphics();
        //var timeLineW = timelineScreenW - (2*h + 4*h + 3*w)// + 8*gap
        scaleTimelineLabel.name = 'scaleTimelineLabel_'+itemName
        scaleTimelineLabel.beginFill(0x222222);
        scaleTimelineLabel.lineStyle(1, 0xffffff, 1);
        scaleTimelineLabel.drawRoundedRect(0,0,timeLineW,h,5)
        scaleTimelineLabel.endFill();
        scaleTimelineLabel.x= left//2*h + 4*h + 2.5*w + 9*gap //timelineScreenW/2 + 2*w +30
        scaleTimelineLabel.y=top+ 2*lineHeight// 2*h+2*gap//timelineScreenH/2 -h/2
        scaleTimelineLabel.zOrder = 200      

        scaleContainer.addChild(prewSFrameCheck)
        scaleContainer.addChild(setSKey)
        scaleContainer.addChild(nextSFrameCheck)
        scaleContainer.addChild(scaleLabel)
        scaleContainer.addChild(scaleText)
        scaleContainer.addChild(scaleX_ValueLabel)
        scaleContainer.addChild(sx_Text)
        scaleContainer.addChild(scaleY_ValueLabel)
        scaleContainer.addChild(sy_Text)
        scaleContainer.addChild(scaleTimelineLabel)
    
        

//展開後的 opacity
        
        // 前一格
        var opacityContainer = new PIXI.Container();

        var prewOFrameCheck = new PIXI.Graphics();

        prewOFrameCheck.name = "prewOFrameCheck_"+ itemName

        prewOFrameCheck.lineStyle(1,0xffffff,1);
        prewOFrameCheck.beginFill(0x555555, 0.6);
        prewOFrameCheck.moveTo(0.5774*h,0)
        prewOFrameCheck.lineTo(0.5774*h, h);
        prewOFrameCheck.lineTo(0,h/2);
        prewOFrameCheck.lineTo(0.5774*h,0);


        prewOFrameCheck.endFill(); 
        prewOFrameCheck.x =  2*h + 4*h + 6*gap//timelineScreenW/2 - w/2 -h 
        prewOFrameCheck.y =  top+ 3*lineHeight//3*h + 3*gap//timelineScreenH/2 -h/2
                    
        
        
        
        //設key的check
        var setOKey = new PIXI.Graphics();
        setOKey.name = "setSKey_"+ itemName
        setOKey.lineStyle(1,0xffffff,1);
        setOKey.beginFill(0x555555, 0.3);
        setOKey.drawCircle(0.5*h,0.5*h,0.4*h)//(0,0,h,h,0.5*h)
        setOKey.endFill(); 
        setOKey.x =  2*h + 5*h + 6*gap//timelineScreenW/2 - w/2 -4*h - 3*gap// -h
        setOKey.y = top+ 3*lineHeight//3*h +3*gap// timelineScreenH/2 -h/2
        
        
      // 下一格
        var nextOFrameCheck = new PIXI.Graphics();
        nextOFrameCheck.name = "nextOFrameCheck_"+ itemName

        nextOFrameCheck.lineStyle(1,0xffffff,1);
        nextOFrameCheck.beginFill(0x555555, 0.6);
        nextOFrameCheck.moveTo(0,0)
        nextOFrameCheck.lineTo(0, h);
        nextOFrameCheck.lineTo(0.5774*h,h/2);
        nextOFrameCheck.lineTo(0,0);


        nextOFrameCheck.endFill(); 
        nextOFrameCheck.x =  2*h + 6*h + 7*gap//timelineScreenW/2 - w/2 -h 
        nextOFrameCheck.y =  top+ 3*lineHeight// 3*h + 3*gap//timelineScreenH/2 -h/2
                      
        
        
        
        var opacityLabel = new PIXI.Graphics();
        opacityLabel.name = 'opacityLabel_'+itemName
        opacityLabel.beginFill(0x555555);
        opacityLabel.lineStyle(1, 0xffffff, 1);
        opacityLabel.drawRoundedRect(0,0,w,h,5)
        opacityLabel.endFill();
        opacityLabel.x= 2*h + 6*h + 10*gap //timelineScreenW/2 -w/2
        opacityLabel.y=  top+ 3*lineHeight//3*h + 3*gap//timelineScreenH/2 -h/2
        opacityLabel.zOrder = 200
        
        var opacityText = new PIXI.Text('opacity',style);
        opacityText.x = 2*h + 7*h + 7*gap +w/2//timelineScreenW/2
        opacityText.y = 0.5*h +  top+ 3*lineHeight//3*h + 3*gap// timelineScreenH/2
        opacityText.zOrder = 300
        opacityText.anchor.set(0.5);
 
        var opacity_ValueLabel = new PIXI.Graphics();
        opacity_ValueLabel.name = 'opacity_ValueLabel_'+itemName
        opacity_ValueLabel.beginFill(0x222222);
        opacity_ValueLabel.lineStyle(1, 0xffffff, 1);
        opacity_ValueLabel.drawRoundedRect(0,0,w+gap,h,5)
        opacity_ValueLabel.endFill();
        opacity_ValueLabel.x= 2*h + 4*h + 1.5*w + 7*gap//timelineScreenW/2 -w/2
        opacity_ValueLabel.y=  top+ 3*lineHeight//3*h + 3*gap//timelineScreenH/2 -h/2
        opacity_ValueLabel.zOrder = 200
        
        var opacity_Text = new PIXI.Text('opacity...',style);
        opacity_Text.x =2*h + 4*h + 2*w + 7*gap//timelineScreenW/2
        opacity_Text.y = 0.5*h + top+ 3*lineHeight// 3*h + 3*gap// timelineScreenH/2
        opacity_Text.zOrder = 300
        opacity_Text.anchor.set(0.5);    
        
        
        // position value timeline 的底部
        var opacityTimelineLabel = new PIXI.Graphics();
        //var timeLineW = timelineScreenW - (2*h + 4*h + 3*w)// + 8*gap
        opacityTimelineLabel.name = 'opacityTimelineLabel_'+itemName
        opacityTimelineLabel.beginFill(0x222222);
        opacityTimelineLabel.lineStyle(1, 0xffffff, 1);
        opacityTimelineLabel.drawRoundedRect(0,0,timeLineW,h,5)
        opacityTimelineLabel.endFill();
        opacityTimelineLabel.x= left//2*h + 4*h + 2.5*w + 9*gap //timelineScreenW/2 + 2*w +30
        opacityTimelineLabel.y=  top+ 3*lineHeight//3*h+3*gap//timelineScreenH/2 -h/2
        opacityTimelineLabel.zOrder = 200      

        opacityContainer.addChild(prewOFrameCheck)
        opacityContainer.addChild(setOKey)
        opacityContainer.addChild(nextOFrameCheck)
        opacityContainer.addChild(opacityLabel)
        opacityContainer.addChild(opacityText)
        opacityContainer.addChild(opacity_ValueLabel)
        opacityContainer.addChild(opacity_Text)
        opacityContainer.addChild(opacityTimelineLabel)
     
        

        

//展開後的 rotation
        
        // 前一格
        var rotationContainer = new PIXI.Container();

        var prewRFrameCheck = new PIXI.Graphics();

        prewRFrameCheck.name = "prewRFrameCheck_"+ itemName

        prewRFrameCheck.lineStyle(1,0xffffff,1);
        prewRFrameCheck.beginFill(0x555555, 0.6);
        prewRFrameCheck.moveTo(0.5774*h,0)
        prewRFrameCheck.lineTo(0.5774*h, h);
        prewRFrameCheck.lineTo(0,h/2);
        prewRFrameCheck.lineTo(0.5774*h,0);


        prewRFrameCheck.endFill(); 
        prewRFrameCheck.x =  2*h + 4*h + 6*gap//timelineScreenW/2 - w/2 -h 
        prewRFrameCheck.y =   top+ 4*lineHeight//4*h + 4*gap//timelineScreenH/2 -h/2
                    
        
        
        
        //設key的check
        var setRKey = new PIXI.Graphics();
        setRKey.name = "setRKey_"+ itemName
        setRKey.lineStyle(1,0xffffff,1);
        setRKey.beginFill(0x555555, 0.3);
        setRKey.drawCircle(0.5*h,0.5*h,0.4*h)//(0,0,h,h,0.5*h)
        setRKey.endFill(); 
        setRKey.x =  2*h + 5*h + 6*gap//timelineScreenW/2 - w/2 -4*h - 3*gap// -h
        setRKey.y =top+ 4*lineHeight//4*h +4*gap// timelineScreenH/2 -h/2
        
        
      // 下一格
        var nextRFrameCheck = new PIXI.Graphics();
        nextRFrameCheck.name = "nextRFrameCheck_"+ itemName

        nextRFrameCheck.lineStyle(1,0xffffff,1);
        nextRFrameCheck.beginFill(0x555555, 0.6);
        nextRFrameCheck.moveTo(0,0)
        nextRFrameCheck.lineTo(0, h);
        nextRFrameCheck.lineTo(0.5774*h,h/2);
        nextRFrameCheck.lineTo(0,0);


        nextRFrameCheck.endFill(); 
        nextRFrameCheck.x =  2*h + 6*h + 7*gap//timelineScreenW/2 - w/2 -h 
        nextRFrameCheck.y =  top+ 4*lineHeight//4*h + 4*gap//timelineScreenH/2 -h/2
                      
        
        
        
        var rotationLabel = new PIXI.Graphics();
        rotationLabel.name = 'rotationLabel_'+itemName
        rotationLabel.beginFill(0x555555);
        rotationLabel.lineStyle(1, 0xffffff, 1);
        rotationLabel.drawRoundedRect(0,0,w,h,5)
        rotationLabel.endFill();
        rotationLabel.x= 2*h + 6*h + 10*gap //timelineScreenW/2 -w/2
        rotationLabel.y= top+ 4*lineHeight//4*h + 4*gap//timelineScreenH/2 -h/2
        rotationLabel.zOrder = 200
        
        var rotationText = new PIXI.Text('rotation',style);
        rotationText.x = 2*h + 7*h + 7*gap +w/2//timelineScreenW/2
        rotationText.y = 0.5*h + top+ 4*lineHeight//4*h + 4*gap// timelineScreenH/2
        rotationText.zOrder = 300
        rotationText.anchor.set(0.5);
 
        var rotation_ValueLabel = new PIXI.Graphics();
        rotation_ValueLabel.name = 'rotation_ValueLabel_'+itemName
        rotation_ValueLabel.beginFill(0x222222);
        rotation_ValueLabel.lineStyle(1, 0xffffff, 1);
        rotation_ValueLabel.drawRoundedRect(0,0,w+gap,h,5)
        rotation_ValueLabel.endFill();
        rotation_ValueLabel.x= 2*h + 4*h + 1.5*w + 7*gap//timelineScreenW/2 -w/2
        rotation_ValueLabel.y= top+ 4*lineHeight//4*h + 4*gap//timelineScreenH/2 -h/2
        rotation_ValueLabel.zOrder = 200
        
        var rotation_Text = new PIXI.Text('rotation...',style);
        rotation_Text.x =2*h + 4*h + 2*w + 7*gap//timelineScreenW/2
        rotation_Text.y = 0.5*h + top+ 4*lineHeight//4*h + 4*gap// timelineScreenH/2
        rotation_Text.zOrder = 300
        rotation_Text.anchor.set(0.5);    
        
        
        // position value timeline 的底部
        var rotationTimelineLabel = new PIXI.Graphics();
        //var timeLineW = timelineScreenW - (2*h + 4*h + 3*w)// + 8*gap
        rotationTimelineLabel.name = 'rotationTimelineLabel_'+itemName
        rotationTimelineLabel.beginFill(0x222222);
        rotationTimelineLabel.lineStyle(1, 0xffffff, 1);
        rotationTimelineLabel.drawRoundedRect(0,0,timeLineW,h,5)
        rotationTimelineLabel.endFill();
        rotationTimelineLabel.x= left//2*h + 4*h + 2.5*w + 9*gap //timelineScreenW/2 + 2*w +30
        rotationTimelineLabel.y= top+ 4*lineHeight//4*h+4*gap//timelineScreenH/2 -h/2
        rotationTimelineLabel.zOrder = 200      

        rotationContainer.addChild(prewRFrameCheck)
        rotationContainer.addChild(setRKey)
        rotationContainer.addChild(nextRFrameCheck)
        rotationContainer.addChild(rotationLabel)
        rotationContainer.addChild(rotationText)
        rotationContainer.addChild(rotation_ValueLabel)
        rotationContainer.addChild(rotation_Text)
        rotationContainer.addChild(rotationTimelineLabel)
            
        
        
        
        itemLabel.addChild(itemNameLabel)
        itemLabel.addChild(itemNameText)
        itemLabel.addChild(visCheck)
        itemLabel.addChild(dragCheck)
        itemLabel.addChild(soloVisCheck)
        itemLabel.addChild(extTimelineCheck)
        itemLabel.addChild(serNoLabel)
        itemLabel.addChild(serNoText)
       
        

        itemLabel.addChild(maskLabel)
        itemLabel.addChild(maskText)
        itemLabel.addChild(blendMode)
        itemLabel.addChild(blendText)
        itemLabel.addChild(timelineBGLabel)
        itemLabel.addChild(timelineClipLabel)

        
        itemLabel.addChild(positionContainer) // add position timeline
        itemLabel.addChild(scaleContainer) // add scale timeline
        itemLabel.addChild(opacityContainer) // add opacityContainer timeline 
        itemLabel.addChild(rotationContainer)
       // var scaleChild = [prewSFrameCheck,setSKey,nextSFrameCheck,scaleLabel,scaleText,scaleX_ValueLabel,sx_Text,scaleY_ValueLabel,sy_Text]
      
        //itemLabel.pivot.x =  itemLabel.width/2
        //itemLabel.x = timelineScreenW/2 - itemLabel.width/2 + w/2 +2*h +20

        labelContainer.addChild(itemLabel)
       // timelineApp.stage.addChild(labelContainer)
        
        
        
    
       // return timelinePanel
    };
    

function createTimelineS(pixiApp,h,left,top,index){
    var gap = 10
    console.log('hhhh',h)
    var itemTimelineContainer = new PIXI.Container() 
    var itemTimelineLabel = new PIXI.Graphics();
    var timeLineW = pixiApp.renderer.screen.width - 2*gap
    itemTimelineLabel.beginFill(0x999999);
    itemTimelineLabel.lineStyle(1, 0xffffff, 1);
    itemTimelineLabel.drawRoundedRect(0,0,200,h,5)
    itemTimelineLabel.endFill();
   // itemTimelineLabel.x = gap
    itemTimelineContainer.y =h*index
    itemTimelineContainer.addChild(itemTimelineLabel)
    pixiApp.stage.addChild(itemTimelineContainer)
    
    
}


function creatTimelineRule(pixiApp,rangeStart,rangeEnd,timelineStart,timelineEnd){
    
    var h = 32
    var w = 200
    var timelineScreenW = pixiApp.renderer.screen.width
    var timelineScreenH = pixiApp.renderer.screen.height        
    var gap = 10
    var left = 2*h + 4*h + 2.5*w + 9*gap
    var top = 0
    var style = {
        fontWeight: 'normal',
        fontSize: h/2,
        fontFamily: 'Arial',
        fill: '#ffffff',
        align: 'center',
      //  stroke: '#FFFFFF',
        strokeThickness: 1
        };
        
        //console.log('screenW',screenW,w)    
    
    
    
    
    var inputField = new PixiTextInput("hello",style)
    pixiApp.stage.addChild(inputField)
    
    
    var rulerContainer = new PIXI.Container()
    rulerContainer.name = 'rulerContainer'
    var rulerTimelineLabel = new PIXI.Graphics();
    var timeLineW =timelineScreenW - (2*h + 4*h + 3*w)
    rulerTimelineLabel.name = 'ruleTimelineLabel'
    rulerTimelineLabel.beginFill(0x999999);
    rulerTimelineLabel.lineStyle(1, 0xffffff, );
    rulerTimelineLabel.drawRoundedRect(0,0,timeLineW,1.5*h,5)
    rulerTimelineLabel.endFill();
    rulerTimelineLabel.x= left//2*h + 4*h + 2.5*w + 9*gap //timelineScreenW/2 + 2*w +30
    rulerTimelineLabel.y= top//0//timelineScreenH/2 -h/2
    rulerTimelineLabel.zOrder = 200   
        
    rulerContainer.addChild(rulerTimelineLabel)
    
    
    var vLineCount = rangeEnd -rangeStart +1
    var VlineSpaceCount =vLineCount -1
    var vLineSpace = Math.floor(timeLineW / VlineSpaceCount)
  
    
    console.log('vLineSpace',vLineSpace)
    
    //draw vLine
    var rulerTimelineVLline = new PIXI.Graphics();
    rulerContainer.addChild(rulerTimelineVLline)

    for(var i=0;i<vLineCount;i++){
        rulerTimelineVLline.name = 'rulerTimelineVLline'
        rulerTimelineVLline.beginFill(0xffffff);
        rulerTimelineVLline.lineStyle(1, 0xffffff, 0.5);
        rulerTimelineVLline.moveTo(0+vLineSpace*i,0)
        rulerTimelineVLline.lineTo(0+vLineSpace*i, h/2);
        rulerTimelineVLline.endFill(); 
        rulerTimelineVLline.zOrder=300
        rulerTimelineVLline.x= left
        rulerTimelineVLline.y= h/2


    }
    
    
        
    pixiApp.stage.addChild(rulerContainer)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    };
    