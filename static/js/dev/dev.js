ithz.dev=function(){
    var me={},rl=10;
    var tree=function(o,nv){
        if(typeof(nv)=="undefined"){nv=1;}
        else if(nv>rl){return ["..."];}
        else{nv++;}
        var c,i,j,l,n,tr=[];
        for(i in o){
            n={
                "name":i,
                "path":i,
                "type":typeof(o[i]),
                "ref":o[i]
            };
            tr[tr.length]=n;
            if(n.type=="object"){
                c=tree(o[i],nv);
                for(j=0,l=c.length;j<l;j++){
                    c[j].path=i+"."+c[j].path;
                    tr[tr.length]=c[j];
                }
            }
        }
        return tr;
    };
    me.tree=function(){
        var c="ithz",i,l;
        var r=window[c];
        var tr=tree(r);
        for(i=0,l=tr.length;i<l;i++){
            tr[i].path=c+"."+tr[i].path;
        };
        tr.splice(0,0,{"name":c,"path":c,"type":typeof(r),"ref":r});
        tr.human=function(){
            var me=this;
            var p,i,l,j,m,tr=[];
            for(i=0,l=me.length;i<l;i++){
                p="";
                for(j=0,m=me[i].path.replace(new RegExp('[^.]',"g"),'').length;j<m;j++){p+="    ";}
                tr[tr.length]=p+me[i].path+" ("+me[i].type+")";
            }
            return tr;
        };
        return tr;
    };
    return me;
}();
ithz.nnm.loaded("dev");
