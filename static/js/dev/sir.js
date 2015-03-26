ithz.ctl.sir=function(){
    var cnode=ithz.uts.createNode,ctext=ithz.uts.createTextNode,addEvent=ithz.uts.addEvent,$def=ithz.uts.$def,$=ithz.uts.$;
    var me={};
    var iheight=80;
    var itemselected=function(r,a,e){
        e.href=a.href.toString().replace(ithz.uts.vars.pagedomain,"");
        if($def("onselect",r)){
            r.onselect(e);
        }
    };
    me.replace=function(r,kow,fp){
        var m=cnode("li"),n=cnode("iframe"),c=cnode("div"),t=ctext("Loading..."),keep=(typeof(kow)=="undefined")?false:!!kow;
        var gdoc=function(n){
            return ($def("contentDocument",n)?n.contentDocument:$def("contentWindow",n)?n.contentWindow.document:null);
        };
        var fakevent=function(vn){
            if(typeof(r.r["on"+vn])=="function"){
                r.r["on"+vn]({"target":me});
            }
        };
        var topparent=(fp)?fp:document.body;
        m.loading=false;
        c.className="ufr_loading";
        r.style.height="auto";
        n.style.display="block";
        n.style.border="0";
        n.style.width="100%";
        n.style.visibility="hidden";
        n.style.height="0px";
        n.src="/dialog/images";
        if(!$def("hfix",r.r)){r.r.hfix=0;}
        r.r.relocate=function(){
            try{
                var p=ithz.page.coords(n,topparent),ph=ithz.page.height(),h=gdoc(n).body.scrollHeight;
                if((keep)&&((p[1]+h+r.r.hfix)>ph)){
                    h=ph-p[1]-r.r.hfix;
                }
                n.style.height=h+"px";
                //n.style.width=doc.body.scrollWidth+"px";
            }catch(e){
                void(0);
            }
        };
        
        addEvent(n,"load",function(){
            var i,l,doc=gdoc(n);
            m.loading=false;
            n.style.visibility="visible";
            c.style.display="none";
            if(doc){
                var f=ithz.uts.$tag("a",doc);
                for(i=0,l=f.length;i<l;i++){
                    if(f[i].href.indexOf("/file/")>-1){
                        addEvent(f[i],"click",function(a){return function(e){itemselected(r,a,e);return false;};}(f[i]));
                    }else{
                        addEvent(f[i],"click",function(){n.style.height="0px";n.style.visibility="hidden";c.style.display="block";});
                    }
                }
            }
            fakevent("load");
        });
        r.r.refresh=function(){
            var doc=$def("contentDocument",n)?n.contentDocument:$def("contentWindow",n)?n.contentWindow.document:null;
            if(doc){
                doc.location.reload();
            }
        };
        
        c.appendChild(t);
        m.appendChild(n);
        m.appendChild(c);
        ithz.uts.insertFirst(m,r);
    };
    return me;
}();
ithz.nnm.loaded("sir");
