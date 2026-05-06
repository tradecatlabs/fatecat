/*紫微斗數 Chinese Astrology Zi Wei Dou Shu*/
var ziwei = {
	y:null, m:null, d:null, h:null, g:null, l:null, b:null, f:null, s4:null, z:null,
	yS:null, mS:null, dS:null, LunarDay:null, ShengXiao:null,
	y1Pos:null,	y2Pos:null,	hPos:null,	lPos:null,	bPos:null,	zPos:null, Palce:null,
	Place12:null,
	//排紫微命盤
	computeZiWei:function (y_Solar,m_Solar,d_Solar,h_Solar,g_Solar){
		//y:年,m:月,d:日,h:時,g:性別,l:命宮,b:身宮,f:五行局,s:起紫微表,s4:四化星;
		yS=y_Solar;
		mS=m_Solar;
		dS=d_Solar;
		//取得農曆時辰，排紫微命盤
		Lunar(0,yS,mS,dS);
		y=HeavenlyStems[(yS - 4) % 10]+EarthlyBranches[(yS - 4) % 12];
		m=lunar.m;
		d=lunar.d;
		h=h_Solar;
		g=g_Solar;
		//年:天干地支
		y1Pos=HeavenlyStems.indexOf(y.substring(0,1));
		y2Pos=EarthlyBranches.indexOf(y.substring(1,2));
		//時:地支
		hPos=EarthlyBranches.indexOf(h);	
		//設定紫微斗數
		this.setZiwei(d);
		//stepSetStar
		this.stepSetStar(y,m,d,h);
		return Place12;
	},
	//CenterPart↑↓
	getLunarDay:function(){return GanGB[gan.y]+ZhiGB[zhi.y]+" 年 "+(lunar.l?"閏":"")+lunar.m+" 月 "+lunar.d+" 日 " + h + " 時";},
	getSolarDay:function(){return yS+ " 年 " + mS + " 月 " + dS + " 日" + h + " 時";},
	getShengXiao:function(){return ShengXiaoGB[(yS - 4) % 12];},
	getFiveElement:function(){return f;},
	getYinYangGender:function(){return YinYang[y1Pos%2]+(g=="M"?"男":"女");},
	//CenterPart↑
	getStarArr:function (STAR,size,pos){
		var starArray = new Array();
		for (i=0;i<size;i++){ starArray[i]=STAR[i][pos]; } return starArray;
	},
	getStarArrByPosArr:function (STAR,size,PosArr){
		var starArray = new Array();
		for (i=0;i<size;i++){ starArray[i]=STAR[i][PosArr[i]]; } return starArray;
	},
	putS04Str:function (starName,STAR){
		return (STAR.indexOf(starName)>=0)?"<b>"+StarM_S04[STAR.indexOf(starName)].substring(1,2)+"</b>":"　";
	},
	getS04Str:function (starName,STAR){
		return (STAR.indexOf(starName)>=0)?StarM_S04[STAR.indexOf(starName)]:"";
	},
	setZiwei:function (d){
    	//重排宮位
		ziweiUI.clearPalce();
    	//安十二宮，安命宮、身宮
		l=EarthlyBranches[((12-hPos)+1+m*1.0)%12];
		b=EarthlyBranches[(12-((22-hPos)+1-m*1.0)%12)%12];
		lPos=EarthlyBranches.indexOf(l);
		bPos=EarthlyBranches.indexOf(b);
		//安五行局
		f=FiveElements[FiveEleArr[y1Pos%5][((lPos-(lPos%2==0?0:1))/2)%6]];
		//起紫微表
		z=EarthlyBranches[FiveEleTable[FiveElements.indexOf(f)][d-1]];
		zPos=EarthlyBranches.indexOf(z);
	},
	stepSetStar:function (y,m,d,h){
		//準備星星
		//0:紫微,1:天機,2:太陽,3:武曲,4:天同,5:廉貞,6:天府,7:太陰,8:貪狼,9:巨門,10:天相,11:天梁,12:七殺,13:破軍
		var s14=Star_A14[zPos];
		var sZ06=this.getStarArr(Star_Z06,7,zPos);
		var sT08=this.getStarArr(Star_T08,8,sZ06[6]);
		//0:文昌 1:文曲 (時) 2:左輔 3:右弼 (月) 4:天魁 5:天鉞 6:祿存(年干)
		var sG07=this.getStarArrByPosArr(Star_G07,7,[hPos,hPos,m-1,m-1,y1Pos,y1Pos,y1Pos]);
		//四化星
		var sS04=this.getStarArr(Star_S04,4,y1Pos);
		//六凶星
		var sB06=[Star_B06[0][y1Pos],Star_B06[1][y1Pos],Star_B06[2][y2Pos%4][hPos],Star_B06[3][y2Pos%4][hPos],Star_B06[4][hPos],Star_B06[5][hPos] ];
		//其他
		var OS05=this.getStarArr(Star_OS5,5,y2Pos);
		Place12=new Array(12);
		//準備開始組星星
		for (i=0;i<12;i++){
			var StarA,StarB,StarC,Star6,lenStar=[0,0,0,0];
			StarA=[];StarB=[];StarC=[];Star6=[];
			//紫微星系 & 六凶星 
			for (k=0;k<6;k++){
				if (sZ06[k]==i){ StarA[lenStar[0]]=StarM_A14[k]+this.getS04Str(StarM_A14[k],sS04); lenStar[0]+=1; }
				if (sB06[k]==i){ StarB[lenStar[1]]=StarM_B06[k]; lenStar[1]+=1;}
			}
			//天府星系
			for (k=0;k<8;k++){
				if (sT08[k]==i){ StarA[lenStar[0]]=StarM_A14[k+6]+this.getS04Str(StarM_A14[k+6],sS04); lenStar[0]+=1; }
			}
			//六吉星
			for (k=0;k<7;k++){
				if (sG07[k]==i){ Star6[lenStar[3]]=StarM_A07[k]+this.getS04Str(StarM_A07[k],sS04); lenStar[3]+=1; }
			}
			//其他星矅StarO_S0.length
			for (k=0;k<5;k++){
				if (OS05[k]==i){ StarC[lenStar[2]]=StarO_S05[k]; lenStar[2]+=1;}
			}
			//塞入位置
	  		Place12[i]={
	  			"MangA": HeavenlyStems[((y1Pos%5)*2+(i<2?i+2:i)%10)%10]+"<br/>"+EarthlyBranches[i],
	  			"MangB": Palace[(12-lPos+i)%12],
	  			"MangC": (bPos==i?Palace[12]:""),
	  			"StarA": StarA,"StarB": StarB,"StarC": StarC,"Star6": Star6
	  		};
	  	}
	},
	getDaShian:function (){
		//大限資料準備
		var DaShianYear=DaShian[FiveElements.indexOf(f)];
		var MangDirection=y1Pos%2; MangDirection+=(g=="M")?1:0;
		//小限資料準備
		var SiaoShianYear,SiaoShianStr,SiaoPlace;
		switch(y2Pos){
			case 2:  case 6: case 10: SiaoShianYear=4; break;
			case 8:  case 0: case 4:  SiaoShianYear=11; break;
			case 5:  case 9: case 1:  SiaoShianYear=7; break;
			case 11: case 3: case 7:  SiaoShianYear=1; break;
		}
		var DShian=new Array(10);
		var SShian=new Array(10);
		for (i=0;i<12;i++){
			//起大限表
			var DSY=MangDirection==1?DaShianYear+i*10:(DaShianYear-i*10+120)%120;
	  		//起小限表
	  		SiaoShianStr="";
			for (j=0;j<6;j++){
				SiaoShianStr+=","+(j*12+i+1);
			}
			SiaoShianStr=SiaoShianStr.substring(1) + " ... ";
			SiaoPlace=(g=="M")?((SiaoShianYear+i)%12+1).toString():((SiaoShianYear-i+12)%12+1).toString();
			DShian[(i+lPos)%12+1]=DSY.toString()+" - "+(DSY+9).toString();
			SShian[SiaoPlace]=SiaoShianStr;
		}
		return {"DShian":DShian,"SShian":SShian};
	}
};
