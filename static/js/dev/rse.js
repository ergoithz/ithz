ithz.ctl.rse=function(){
    var me={};
    var $def=ithz.uts.$def,addev=ithz.uts.addEvent,addnode=ithz.uts.createNode,
        addtext=ithz.uts.createTextNode,stop=ithz.uts.stopEvent,clearNode=ithz.uts.clearNode;
    var selectClass="select_replacer",selectClickedClass="select_replacer_clicked";
    me.rselect=function(s){
        var o=s.options,d=addnode("div"),u=addnode("ul"),p=addnode("p"),f,i,l,t;
        s.r={"div":d,"ul":u,"p":p,"hidebool":false,"clicked":false,"timeout":null};
        f=function(){s.r.div.className=(s.r.clicked)?selectClass:selectClickedClass;s.r.clicked=!s.r.clicked;};
        s.r.click=function(){
            if(ithz.trs){
                if(s.r.clicked){s.r.ul.oncontract=f;ithz.trs.contract(s.r.ul,0.5);}
                else{f();ithz.trs.expand(s.r.ul,0.5);}
            }else{f();}
            };
        s.r.change=function(){if(s&&s.r.p){clearNode(s.r.p);s.r.p.appendChild(addtext(s.options[s.selectedIndex].text));}};
        s.r.hide=function(e){
            if(s&&s.r&&s.r.hidebool&&s.r.clicked){
                if(!e){stop();}
                else{stop(e);}
                s.r.click();
                s.r.hidebool=false;
            }
        };
        s.r.option=function(i){s.selectedIndex=i;s.r.change();};
        s.r.div.onmouseover=function(){s.r.hidebool=false;/*clearInterval(s.r.timeout);*/};
        s.r.div.onmouseout=function(){s.r.hidebool=true;/*s.r.timeout=setTimeout(s.r.hide,2000);*/};
        d.className=selectClass;
        d.onclick=function(){s.r.click();};
        d.appendChild(p);
        d.appendChild(u);
        for (i=0;o[i];i++){
            l=addnode("li");
            t=addtext(o[i].text);
            l.onclick=function(s,i){return function(){s.r.option(i);};}(s,i);
            l.appendChild(t);
            u.appendChild(l);
        }
        s.style.display = "none";
        ithz.uts.insertAfter(d,s);
        s.r.change();
        addev(s,"change",s.r.change);
        addev(document,"click",s.r.hide);
    };
    return me;
}();
ithz.nnm.loaded("rse");
