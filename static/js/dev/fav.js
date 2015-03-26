ithz.ctl.fav=function(){
    var me={};
    me.faviconize=function(r){
        var n=ithz.uts.getDomain(r.href+""),i=document.createElement("img");
        if(r.stbged){ithz.uts.addEvent(i,"load",function(){ithz.trs.ustbg(r);});}
        i.style.margin="2px";
        i.src=n+"/favicon.ico";
        
        ithz.uts.insertFirst(i,r);
    };
    me.alienize=function(rl){
        if(typeof(ids)=="string"){rl=[rl];}
        var i,il;
        for(i=0,il=rl.length;i<il;i++){if((n!=ithz.uts.vars.pagedomain)){me.faviconize(rl[i]);}}
    };
    return me;
}();
ithz.nnm.loaded("fav");
