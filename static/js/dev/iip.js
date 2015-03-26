ithz.ctl.iip=function(){
    var me={},addnode=ithz.uts.createNode,addev=ithz.uts.addEvent,insertAfter=ithz.uts.insertAfter;
    me.intinput=function(r){
        var a=addnode("input"),b=addnode("input"),c=addnode("input"),rst,llv;
        llv=function(){
            if(/^\d*$|^-\d*$/.test(r.value)){r.r.lastValidValue=r.value;}
            else{r.value=r.r.lastValidValue;}
        };
        r.style.display="inline-block";
        a.type="button";a.value="-";a.className="intinput_button";a.title="Deduct";
        b.type="button";b.value="+";b.className="intinput_button";b.title="Add";
        c.type="button";c.value="<";c.className="intinput_button";c.title="Reset";
        addev(a,"click",function(){r.value--;});
        addev(b,"click",function(){r.value++;});
        addev(c,"click",function(){r.value=rst;});
        insertAfter(c,r);insertAfter(b,r);insertAfter(a,r);
        r.r.lastValidValue=0;
        llv();
        rst=r.r.lastValidValue;
        addev(r,"keyup",llv);
        addev(r,"change",llv);
    };
    return me;
}();
ithz.nnm.loaded("iip");
