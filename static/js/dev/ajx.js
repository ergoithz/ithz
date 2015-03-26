ithz.ajx=function(){
    var $def=ithz.uts.$def,$=ithz.uts.$,redirect=ithz.uts.redirect;
    var me={};
    var events={
		"json":[],
        "action":[],
        "load":[],
        "error":[],
        "ready":[]
    };
    me.exeCallback=function(id,data){
        var c=events,d=(data)?data:null;
        if($def(id,c)){
            for(var i=c[id].length-1,il=-1;i>il;i--){
                c[id][i](d);
                if(!c[id][i].keep){
                    c[id].splice(i,1);
                }
            }
        }
    };
    me.addCallback=function(id,f,temp){
        var c=events;
        if($def(id,c)){
            f.keep=(!temp);
            c[id][c[id].length]=f;
        }
    };
    me.lastError=null;
    me.json=null;
    me.jsonParse=function(x){
        if($def("JSON")){try{return JSON.parse(x);}catch(e1){}}
        try{return eval("("+x+")");}catch(e2){}
        return null;
    };
    var jsonLoad=function(x,u,fb){
        var j=me.jsonParse(x),noredir=true;
        if(!j){me.exeCallback("error",{'message':'JSON error'});redirect(fb);return false;}
        try{for(var i in j){me.exeCallback("json",{"name":i,"value":j[i]});}}
        catch(e){redirect(fb);return false;}
		me.exeCallback("load");
		me.exeCallback("ready");
        return true;
    };
    var hif=null; //hidden iframe
    var ajax=null;
    var method=-1; //-1 unknown, 0 not supported, 1 iframe, 2 xmlhttp
    var initAjax=function(){
        if((method==-1)||("\v"=="v")){
            var xmlhttp=null;
            if($def("XMLHttpRequest")){xmlhttp=new XMLHttpRequest();}
            else if($def("ActiveXObject")){
                try{xmlhttp=new ActiveXObject("Msxml2.XMLHTTP");}
                catch(e){
                    try{xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");}
                    catch (E){xmlhttp=false;}
                }
            }
            if(xmlhttp){ajax=xmlhttp;method=2;}
            else{
                /* Legacy: using iframe */
                method=1;
                hif=document.createElement("iframe");
                var s=hif.style;
                s.border="0";
                s.height="0px";
                s.width="0px";
                s.visibility="hidden";
                s.position="absolute";
                s.left="0";
                s.top="0";
                document.body.appendChild(hif);
            }
        }
    };
    var getrscback=function(u,f,c){
        var tr=function(){
            var rs=ajax.readyState;
            if(rs==4){
                var rt=ajax.responseText||null;
                if((rt)&&(rt.length)){
                    c(unescape(rt),u,f);
                }
            }else if(rs==404||rs==501){me.lastError=rs;me.exeCallback("error");}};
        return tr;
        };
    me.invokeUrl=function(url,fburl,postparams,form,callback){
        initAjax();
        if (method===0){
            redirect(fburl);
        }else{
            if(!callback){callback=jsonLoad;}
            var usePost=(typeof(postparams)!="undefined");
            if(method==1){
                try{
                    hif.onload=function(){
                        var c="",a=hif.contentWindow.document.body;
                        while(a.firstChild){a=a.firstChild;}
                        callback(unescape(a.textContent),url,fburl);
                        };
                    if (usePost){
                        var doc=hif.contentWindow.document;ta="";
                        //TODO: POST-GET WRAPPER
                        if(postparams.length>0){
                            ta="<input type='text' name='"+
                                postparams
                                .replace("&","'><input type='text' name='")
                                .replace("=","' value='");
                            }
                        doc.open();
                        doc.write("<html><head></head><body><form action='"+url+"' method='POST'>"+ta+"</form></body></html>");
                        doc.close();
                        doc.body.firstChild.submit();
                    }else{hif.src=url;}
                }catch(e){
                    me.lastError=501;
                    me.exeCallback("error");
                    redirect(fburl,500);
                }
            
            }else if(method==2){
                try{
                    ajax.onreadystatechange=getrscback(url,fburl,callback);
                    if(usePost){ajax.open("POST",url,true);}
                    else{ajax.open("GET",url,true);}
                    if(usePost){
                        ajax.setRequestHeader("Content-type","application/x-www-form-urlencoded");
                        ajax.setRequestHeader("Content-length",postparams.length);
                        ajax.setRequestHeader("Connection","close");
                        ajax.send(postparams);
                    }else{
                        ajax.send(null);
                    }
                }catch(e){
                    me.lastError=501;
                    me.exeCallback("error");
                    redirect(fburl,500);
                }
            }
        }
    };
    var extractSection=function(url){
        if(url.search(ithz.uts.vars.pagedomain)>-1){return url.substring(ithz.uts.vars.pagedomain.length);}
        else{return url;}
    };
    var ajaxSection=function(url){
        return ithz.uts.vars.pagedomain+"/ajax"+extractSection(url);
    };
    var current_hash="";
    var enableHashChecking=false;
    var checkLocationInterval=null;
    var updateHash=function(hash){
        enableHashChecking=false;
        document.location.hash=hash;
        current_hash=document.location.hash;
        enableHashChecking=true;
    };
    me.startHashCheck=function(){
        enableHashChecking=true;
        if (!checkLocationInterval){
            checkLocationInterval=setInterval(function(){
                if(enableHashChecking){
                    var newh=document.location.hash;
                    if((newh)&&(newh!=current_hash)){
                        enableHashChecking=false;
                        me.exeCallback("action");
                        var url=document.location.hash.replace(/\#/g,"");
                        updateHash(url);
                        me.invokeUrl(ajaxSection(url));
                    }
                }
            },2000);
        }
    };
    var jsv=/*@cc_on (function(){if(@_jscript_version>5.6){return 1;}return 0;})()||@*/0;
    var ajaxsupported=(($def("XMLHttpRequest")&&$def("DOMParser"))||($def("ActiveXObject")&&(jsv)));
    me.linkWrapper=function(ev,item){
        if(ajaxsupported){
            ithz.uts.stopEvent(ev);
            me.exeCallback("action");
            updateHash(extractSection(item.href));
            me.invokeUrl(ajaxSection(item.href),item.href);
            return false;
        }
        return true;
    };
    var formajaxsupported=((ajaxsupported)&&($def("encodeURIComponent")));
    me.formWrapper=function(ev,item){
        if(formajaxsupported){
            ithz.uts.stopEvent(ev);
            me.exeCallback("action");
            var url=extractSection(item.action);
            var tags=["input","textarea","checkbox","radiobutton","select"];
            var params="";
            for (var i=0,it,il=item.length,j,jl=tags.length;i<il;i++){
                if(item[i].name){
                    for(j=0,it=item[i].nodeName.toLowerCase();j<jl;j++){
                        if(it==tags[j]){
                            params+="&"+item[i].name+"="+encodeURIComponent(item[i].value);
                            break;
                        }
                    }
                }
            }
            updateHash(url);
            me.invokeUrl(ajaxSection(item.action),item.action,params.substring(1),item);
            return false;
        }
        return true;
    }; 
    return me;
}();
ithz.nnm.loaded("ajx");
ithz.nnm.deferExe(["page"],ithz.ajx.startHashCheck);
