/*
* Available modules:
    * Pure JS:
        * fpr fuuuu popup replacer (modal dialogs)
        * xtr xhtml textarea replacer
        * iip integer input replacer
        * rse select replacer
        * fav faviconize links
    * JS + Server-side coded:
        * ufr upload file replacer
        * sir select item replacer
* TODO:
    * http://www.cssblog.es/solucion-a-la-transparencia-png-en-ie-6-ii/
*/
ithz.ctl=function(){
    var me={},$tag=ithz.uts.$tag,$def=ithz.uts.$def,vars=ithz.uts.vars,attr=ithz.uts.attr,makeMap=ithz.uts.makeMap,rp="r",pg=vars.pagedomain;
    var najx=makeMap(pg+"/_ah,"+pg+"/file"), // Non-ajax href prefixes (for rlink)
        cnajx=makeMap(pg+"/admin");
    var notin=function(a,b){
        for(var i in b){if(a.search(i)===0){return false;}}
        return true;
        },into=function(a,b){return !notin(a,b);};
    var rdiv=function(r){
        var i,l,np;
        if(!$def(rp,r)){
            r[rp]={};
            if((r.id)&&(r.id.search("_upfile_")>-1)){
                ithz.uts.clearNode(r);
                np=ithz.uts.nodeParents(r);
                for(i=0,l=np.length;i<l;i++){
                    if(np[i].nodeName.toLowerCase()=="form"){
                        np[i].action="javascript:";
                        break;
                    }
                }
                r.style.height="20px";
                ithz.trs.stbg(r,"/style/load2.gif",false,"left","center");
                ithz.nnm.demmand(["ufr"],function(){ithz.ctl.ufr.ruform(r);ithz.trs.ustbg(r);});
            }
        }
    };
    var groups={};
    var rli=function(r){
        if(!$def(rp,r)){
            r[rp]={};
            if((r.id)&&(r.id.search("_hide_")>-1)){
                var a,b,c,o,s,h;
                a=r.id.split("_hide_");a=a[a.length-1]||"default";
                if(a in groups){o=groups[a];o[o.length]=r;}
                else{
                    b=ithz.uts.createNode("li");
                    b.appendChild(ithz.uts.createTextNode("Show advanced options"));
                    b.className="advanced_show";
                    c=ithz.uts.createNode("li");
                    c.appendChild(ithz.uts.createTextNode("Hide advanced options"));
                    c.className="advanced_hide";
                    o=[c,r];
                    ithz.uts.insertBefore(b,r);
                    ithz.uts.insertBefore(c,r);
                    o.s=function(){
                        for(var i=0,l=o.length;i<l;i++){o[i].style.display="block";}
                        b.style.display="none";
                        };
                    o.h=function(){
                        for(var i=0,l=o.length;i<l;i++){o[i].style.display="none";}
                        b.style.display="block";
                        };
                    b.onclick=o.s;
                    c.onclick=o.h;
                    groups[a]=o;
                }
            }
        }
    };
    var rselect=function(r){
        if((r.id)&&(!$def(rp,r))){
            r[rp]={};
            ithz.trs.stbg(r,"/style/load.gif",false,"left","center");
            ithz.nnm.demmand(["rse"],function(){ithz.ctl.rse.rselect(r);ithz.trs.ustbg(r);});
        }
    };
    var rlink=function(r){
        var i,il;
        if(!$def(rp,r)){
            r[rp]={};
            if((r.id)&&(r.id.search("_fav_")>-1)){
                ithz.trs.stbg(r,"/style/load.gif",false,"left","center");
                ithz.nnm.demmand(["fav"],function(){ithz.ctl.fav.faviconize(r);});
            }
            if(notin(r.href,najx)&&(notin(document.location.href,cnajx)||into(r.href,cnajx))&&(r.target!="_blank")&&(r.href.search(vars.pagedomain)===0)){
                ithz.nnm.deferExe(["ajx"],function(){
                    ithz.uts.addEvent(r,"click",function(e){return ithz.ajx.linkWrapper(e,r);});});
            }
        }
    };
    var rtextarea=function(r){
        var i,il;
        if((r.id)&&(!$def(rp,r))){
            r[rp]={};
            if(r.id.search("_xhtml_")>-1){
                ithz.trs.stbg(r,"/style/load.gif",false,"left","top");
                ithz.nnm.demmand(["xtr","fpr"],function(){ithz.ctl.xtr.rta(r);ithz.trs.ustbg(r);});
            }
        }
    };
    var rinput=function(r){
        if((r.id)&&(!$def(rp,r))){
            r[rp]={};
            if((r.type=="text")&&(r.id.search("_int_")>-1)){
                ithz.trs.stbg(r,"/style/load.gif",false,"left","center");
                ithz.nnm.demmand(["iip"],function(){ithz.ctl.iip.intinput(r);ithz.trs.ustbg(r);});
            }else if((r.type=="checkbox")&&(r.id.search("_switch_")>-1)){
                var a=ithz.uts.createNode("div"),b;
                r.style.display="none";
                b=function(){if(r.checked){a.className="check_on";}else{a.className="check_off";}};
                a.onclick=function(){r.checked=!r.checked;b();return false;};
                b();
                ithz.uts.insertBefore(a,r);
            }
            if(r.id.search("_autosubmit_")>-1){
                r.onchange=function(){
                    if(r.value.length){if(r.form.onsubmit){r.form.onsubmit();}
                    r.form.submit();}};
            }
        }
    };
    var rform=function(r){
        if(!$def(rp,r)){
            r[rp]={};
            if((r.action.search(vars.pagedomain)===0)&&((attr(r,"id")||"").search("_noajax_")==-1)){
                ithz.nnm.deferExe(["ajx"],function(){
                    ithz.uts.addEvent(r,"submit",function(e){return ithz.ajx.formWrapper(e,r);});});
            }
        }
    };
    me.jsControls=function(doc){
        var d,i,l,n,td=[],o=doc||document;
        var add=function(a,b){td[td.length]=[a,b];},
        mp={"ol":rdiv,"li":rli,"select":rselect,"a":rlink,"textarea":rtextarea,"input":rinput,"form":rform};
        for(n in mp){
            d=$tag(n,o);
            if(d){for(i=0,l=d.length;i<l;i++){add(mp[n],d[i]);}}
            }
        for(i=0,l=td.length;i<l;i++){td[i][0](td[i][1]);}
        for(i in groups){groups[i].h();}
    };
    return me;
}();
ithz.nnm.deferExe(["ajx","ctl","trs"],
    function(){
        ithz.ajx.addCallback("load",function(){ithz.ctl.jsControls();});
    });
ithz.uts.addEvent(window,"load",function(){ithz.ctl.jsControls();});
ithz.nnm.loaded("ctl");
