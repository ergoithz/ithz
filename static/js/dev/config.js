ithz.nnm.path="/js";
ithz.nnm.add(["rhp","trs","ajx","css","ctl"]);
ithz.nnm.deferExe(["ajx","page"],function(){
	// AJX BEHAVIOR
	//TODO: make it on ctl
	var $=ithz.uts.$,b=ithz.trs;
	var el={
		"menu":$("topmenu"),
		"side":$("sidemenu"),
		"content":$("pagecontent"),
		"gentime":$("gentime"),
		};
	ithz.ajx.addCallback("json",function(d){
		if(d.name in el){
			ithz.uts.clearNode(el[d.name]);
			if('\v'=='v'){el[d.name].innerHTML=d.value;} //IE is a bullshit
			else{ithz.rhp.HTMLtoNODE(d.value,el[d.name]);}
            if(d.name=="side"){
                if(d.value.length==0){document.body.className="nomenu";}
                else{document.body.className="";}
                }
            }
        else if(d.name=="title"){document.title=d.value;}
		});
	
	// ANIMATIONS
	/*
	var imgs=["/style/clouds.gif","/style/rain.gif","/style/thunder.png"];
	if(document.images){
		for(var i=0,j=imgs.length;i<j;i++){
			c1=new Image(); 
			c1.src=imgs[i];
		}
	}
	*/
	var l1=$("l1"),l2=$("l2"),l3=$("l3");
	// Sky animation (sm: 0 clouds; 1 rain; 2 lighting)
	/*
	var sky={},r=function(m){return parseInt(Math.random()*m);};
	sky.sm=0;
	sky.osm=0;
	sky.i=new b.bgmoveIter(1000);

	sky.u=function(m){
		sky.osm=sky.sm;
		sky.sm=m;
		sky.i.stop();
		sky.i.clear();
		if(m==0){
			b.stbg(l1,imgs[0],"repeat-x",0,"20px");
			sky.i.add(l1,-1,0,1910,142);
			sky.i.timeout=1000;
			sky.i.start(); 
		}else if(m==1){
			b.stbg(l1,imgs[1],"repeat-x",0,0);
			sky.i.add(l1,490,0,2000,206);
			sky.i.timeout=300;
			sky.i.start();
		}else if(m==2){
			b.stbg(l1,imgs[2],0,"center",0);
		}
	};
	sky.t=function(t){setTimeout(sky.r,t);};
	sky.r=function(){
		if(sky.sm==0){
			if(r(3)>1){sky.sm+=1;}
			if(sky.osm!=0){
				sky.osm=0;
				l1.onfadein=function(){
					sky.t(10000);
				};
				l1.onfadeout=function(){
					sky.u(0);
					b.fadeIn(l1,5);
				};
				b.fadeOut(l1,5);
			}else{
				sky.t(5000);
			}
		}else if(sky.sm==1){
			sky.sm+=r(3)-1;
			if(sky.osm!=1){
				sky.osm=1;
				l1.onfadein=function(){
					sky.t(3000);
				};
				l1.onfadeout=function(){
					sky.u(1);
					b.fadeIn(l1,5);
				};
				b.fadeOut(l1,0.5);
			}else{
				sky.t(3000);
			}
		}else if(sky.sm==2){
			sky.sm=1;
			sky.osm=2;
			sky.u(2);
			sky.t(500);
		}
	};
	sky.u(0);
	sky.r();
	*/
	
	
	// Clouds
	var i1=new b.bgmoveIter(1000);
	b.stbg(l1,0,"repeat-x",0,"20px");
	i1.add(l1,-1,0,1910,142);
	i1.start();
	
	// Gear animation
	/*b.stbg(l3,0,"repeat-x",0,"15px");*/ // Skyline moving
	b.stbg(l2,0,false,"right");
	var i2=new b.bgmoveIter(150,1);
	i2.add(l2,0,-200,171,1200);
	/*i2.add(l3,2,0,1546,232);*/
	ithz.ajx.addCallback("action",i2.start);
	ithz.ajx.addCallback("ready",i2.stop); 
	});
