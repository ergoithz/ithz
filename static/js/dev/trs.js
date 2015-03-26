ithz.trs=function(){
    var me={},$def=ithz.uts.$def;
    var sps=15;
    var sout=1000/sps;
    var transitionStep=function(o){
        var p=Math.cos((o.anicont+=o.anistep)*Math.PI)+1;
        if(o.anicont<=1){
            if(o.anicont>(1-o.anistep)){
                ithz.css.opacity(o,0);
                o.style.height="0px";
                if($def("oncontract",o)){o.oncontract();}
            }else{
                ithz.css.opacity(o,p);
                o.style.height=(o.aniheight*p)+"px";
                setTimeout(function(){transitionStep(o);},sout);
            }
        }else if(o.anicont<=2){
            if(o.anicont>(2-o.anistep)){
                ithz.css.opacity(o,1);
                o.style.height="auto";
                o.style.overflow="visible";
                if($def("onexpand",o)){o.onexpand();}
            }else{
                ithz.css.opacity(o,p);
                o.style.height=(o.aniheight*p)+"px";
                setTimeout(function(){transitionStep(o);},sout);
            }
        }            
    };
    var fadeStep=function(o){
        var p=(Math.cos((o.anicont+=o.anistep)*Math.PI)+1)*o.anie;
        if(o.anicont<=1){
            if(o.anicont>(1-o.anistep)){
                ithz.css.opacity(o,0);
                if($def("onfadeout",o)){o.onfadeout();}
            }else{
                ithz.css.opacity(o,p);
                setTimeout(function(){fadeStep(o);},sout);
            }
        }else if(o.anicont<=2){
            if(o.anicont>(2-o.anistep)){
                ithz.css.opacity(o,o.anie*2);
                if($def("onfadein",o)){o.onfadein();}
            }else{
                ithz.css.opacity(o,p);
                setTimeout(function(){fadeStep(o);},sout);
            }
        }    
    };
    me.expand=function(o,t){
        o.aniheight=o.scrollHeight/2;o.anicont=1;o.anistep=1/(sps*((t)?t:1));
        o.style.overflow="hidden";
        transitionStep(o);
    };
    me.contract=function(o,t){
        if(!t){t=1;}
        var h=o.scrollHeight/2;
        o.aniheight=h;o.anicont=0;o.anistep=1/(sps*t);
        o.style.overflow="hidden";
        transitionStep(o);
    };
    me.fadeIn=function(o,t,end){
        o.anie=(end)?end/2:0.5;
        o.anicont=1;o.anistep=1/(sps*((t)?t:1));
        fadeStep(o);
    };
    me.fadeOut=function(o,t,end){
        o.anie=(end)?end/2:0.5;
        o.anicont=0;o.anistep=1/(sps*((t)?t:1));
        fadeStep(o);
    };
    me.bgmoveIter=function(t,c){
        // Returns a bg animation interator object. Usage: ...bgmoveiter( <milliseconds timeout> , <boolean (setTimeout if true, setInterval otherwise)> )
        var me={},tb=0,o=[],n=null;
        me.timeout=(t)?t:250;
        me.c=(c)?1:0;
        me.__iter=function(){
            var i,il=o.length;
            for(i=0;i<il;i++){
                if(o[i].bgminc[0]){o[i].bgmpos[0]+=o[i].bgminc[0];if(Math.abs(o[i].bgmpos[0])>=o[i].bgmsize[0]){o[i].bgmpos[0]=0;}}
                if(o[i].bgminc[1]){o[i].bgmpos[1]+=o[i].bgminc[1];if(Math.abs(o[i].bgmpos[1])>=o[i].bgmsize[1]){o[i].bgmpos[1]=0;}}
                if(o[i].bgmposowx){o[i].style.backgroundPosition=o[i].bgmposowx+" "+o[i].bgmpos[1]+"px";}
                else if(o[i].bgmposowy){o[i].style.backgroundPosition=o[i].bgmpos[0]+"px "+o[i].bgmposowy;}
                else{o[i].style.backgroundPosition=o[i].bgmpos[0]+"px "+o[i].bgmpos[1]+"px";}
            }
            if(tb){setTimeout(me.__iter,me.timeout);}
        };
        me.start=function(){
            if(me.c){
                if(!tb){tb=1;me.__iter();}
            }else if(n==null){n=setInterval(me.__iter,me.timeout);}
        };
        me.stop=function(){
            tb=0;
            clearInterval(n);
            n=null;
        };
        me.add=function(n,x,y,w,h){
            n.bgmpos=($def("bgmpos",n))?[n.bgmpos[0],n.bgmpos[1]]:[0,0];
            n.bgminc=[(x)?x:0,(y)?y:0];
            n.bgmsize=[(w)?w:0,(h)?h:0];
            n.bgmiter=me;
            o[o.length]=n;
        };
        me.clear=function(){
            var i,il=o.length;
            for(i=0;i<il;i++){
                o.pop().bgmpos=[0,0];
            }
        };
        return me;
    };    
    me.stbg=function(o,src,r,cx,cy){
        o.stbged=true;
        o.style.backgroundRepeat=(r)?r:"no-repeat";
        if(src){o.style.backgroundImage="url('"+src+"')";}
        if(cx){o.bgmposowx=cx;}
        if(cy){o.bgmposowy=cy;}
        if((cx)&&(cy)){o.style.backgroundPosition=cx+" "+cy;}
        else if((cx)&&(!cy)){o.style.backgroundPosition=cx+" top";}
        else if((!cx)&&(cy)){o.style.backgroundPosition="left "+cy;}
        else{o.style.backgroundPosition="left top";}
    };
    me.ustbg=function(o){
        o.stbged=false;
        o.style.backgroundImage="none";
    };
    return me;
}();

ithz.nnm.loaded("trs");
