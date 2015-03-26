ithz.ctl.fpr=function(){
    var cn=ithz.uts.createNode,$def=ithz.uts.$def,removeElement=ithz.uts.removeElement,
        infirst=ithz.uts.insertFirst,addev=ithz.uts.addEvent,popev=ithz.uts.popEvent,
        clearNode=ithz.uts.clearNode;
    var me={},op=0.7;
    me.dialog=function(d){
        var msk=cn("div"),b=cn("div"),cnt=cn("div"),x=cn("img"),tr;
        var body=(d)?d.body:document.body;
        msk.className="dialogMask";
        b.className="dialogOuter";
        cnt.className="dialogContent";
        b.appendChild(cnt);
        x.className="dialogX";
        x.src="/icons/cross.png";
        cnt.x=x;
        tr=function(){
            var did=-1,me={},visible=false,realized=false;
            var fakevent=function(vn){
                if(typeof(me["on"+vn])=="function"){
                    me["on"+vn]({"target":me});
                }
            };
            var setVisible=function(b){
                var p=(b)?"visible":"hidden";
                msk.visibility=p;
                b.visibility=p;
                x.visibility=p;
            };
            me.onhide=null;
            me.onshow=null;
            me.style=cnt.style;
            me.outer=b;
            me.main=cnt;
            me.mask=msk;
            me.realize=function(){
                me.unrealize();
                setVisible(0);
                infirst(msk,body);
                infirst(b,body);
                infirst(x,body);
                ithz.ctl.jsControls();
                if(did==-1){
                    did=addev(window,"resize",me.relocate);
                }
                fakevent("realize");
                realized=true;
            };
            me.show=function(){
                if(!visible){
                    if(!realized){me.realize();}
                    me.relocate();
                    if($def("trs",ithz)){
                        ithz.css.opacity(msk,0);
                        ithz.css.opacity(b,0);
                        ithz.css.opacity(x,0);
                        msk.onfadein=function(){
                            ithz.trs.fadeIn(b,0.5);
                            ithz.trs.fadeIn(x,0.5);
                            fakevent("show");
                            visible=true;
                        };
                        setVisible(1);
                        ithz.trs.fadeIn(msk,0.5,op);
                    }else{
                        setVisible(1);
                        fakevent("show");
                        visible=true;
                    }
                }
            };
            me.pack=function(o,bfirst){
                if(bfirst){infirst(o,cnt);}
                else{cnt.appendChild(o)}
                if(visible){me.relocate();}
            };
            me.hide=function(){
                if(visible){
                    if($def("trs",ithz)){
                        msk.onfadeout=function(){
                            fakevent("hide");
                            setVisible(0);
                            visible=false;
                        };
                        ithz.trs.fadeOut(x,0.5);
                        ithz.trs.fadeOut(b,0.5);
                        ithz.trs.fadeOut(msk,0.5,op);
                    }else{
                        setVisible(0);
                        fakevent("hide");
                        visible=false;
                    } 
                }          
            };
            me.unrealize=function(){
                if(realized){
                    if(visible){
                        me.hide();
                    }
                    clearNode(cnt);
                    removeElement(msk);
                    removeElement(b);
                    removeElement(x);
                    if(did>-1){
                        popev(window,"resize",did);
                        did=-1;
                    }
                    fakevent("unrealize");
                    realized=false;
                }
            };
            me.relocate=function(){
                var w=ithz.page.width(),h=ithz.page.height();
                var dw=b.scrollWidth,dh=b.scrollHeight;
                var pw=(w-dw)/2,ph=(h-dh)/2;
                b.style.left=pw+"px";
                b.style.top=ph+"px";
                cnt.x.style.left=(pw+dw-26)+"px";
                cnt.x.style.top=(ph+10)+"px";
                };
            return me;
        }();
        addev(msk,"click",tr.hide);
        addev(x,"click",tr.hide);
        return tr;
    };
    return me;
}();
ithz.nnm.loaded("fpr");
