ithz.ctl.ufr=function(){
    var cnode=ithz.uts.createNode,ctext=ithz.uts.createTextNode,addEvent=ithz.uts.addEvent,$def=ithz.uts.$def,$=ithz.uts.$;
    var me={};
    var clearUnused=function(r){
        var i=r.childNodes.length,n=0;
        while(--i>0){
            n++;
            if(r.childNodes[i].loading==false){
                if(n>1){ithz.uts.removeElement(r.childNodes[i]);}
            }
        }
    };
    me.addiframe=function(r,hl){
        var m=cnode("li"),n=cnode("iframe"),c=cnode("div"),t=ctext("Loading...");
        m.loading=false;
        if(hl){c.style.display="none";}
        c.className="ufr_loading";
        r.style.height="auto";
        n.style.display="block";
        n.style.border="0";
        n.style.width="100%";
        n.style.visibility="hidden";
        n.style.height="0px";
        n.src="/dialog/upload";
        var fakevent=function(vn){
            if(typeof(r.r["on"+vn])=="function"){
                r.r["on"+vn]({"target":me});
            }
        };
        addEvent(n,"load",function(){
            var doc,i,l;
            m.loading=false;
            n.style.visibility="visible";
            doc=$def("contentDocument",n)?n.contentDocument:$def("contentWindow",n)?n.contentWindow.document:null;
            if(ithz.css){ithz.css.loadCSS(doc);}
            if(ithz.ctl){ithz.ctl.jsControls(doc);}
            try{
                n.style.height=(doc.body.scrollHeight+1)+"px";
                //n.style.width=doc.body.scrollWidth+"px";
            }catch(e){
                void(0);
            }
            c.style.display="none";
            clearUnused(r);
            if(doc){
                var f=doc.forms;
                for(i=0,l=f.length;i<l;i++){
                    addEvent(f[i],"submit", function(){
                        t.nodeValue="Uploading file...";
                        m.loading=true;
                        n.style.visibility="hidden";
                        n.style.height="0px";
                        c.style.display="block";
                        me.addiframe(r,true);
                        });
                }
            }
            fakevent("load");
        });
        
        c.appendChild(t);
        m.appendChild(n);
        m.appendChild(c);
        ithz.uts.insertFirst(m,r);
        clearUnused(r);
    };
    
    me.ruform=function(r){
        me.addiframe(r);
    };
    return me;
}();
ithz.nnm.loaded("ufr");
