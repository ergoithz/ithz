var df,ns,bc;
df=function(n,s){if(!s){s=window;}return (typeof(s[n])!="undefined");};
ns=function(s){
    var a=window,l=s.split("."),i,n;
    for(i=0,n=l.length;i<n;i++){
        if(!df(l[i],a)){a[l[i]]={};}
        a=a[l[i]];
    }
    return a;
};
ns("ithz");
ithz.main={
    "name":"ithz CMS javascript framework",
    "version":"0.1.3",
    "author":"ergoithz[at]gmail[dot]com",
    "license":"Copyrighted by Felipe A. Hernández. HTML parser under Mozilla software license (source code at /js/rhp.js)"
};
ithz.uts=function(){
    var me={},
        updateEvents=function(o,ev){
            // Aux function for addEvent and popEvent
            o['on'+ev]=function(ge){
                var k=o.mevp,e=(!!ge)?ge:(me.$def("event"))?window.event:null;
                if(o&&o.mev&&o.mev[ev]){
                    var evts=o.mev[ev];
                    for(var i=0,len=o.mev[ev].length;i<len;i++){if(evts[i](e)===false){k&=0;}}
                }
                return !!k;
            };
        };
    me.xmlns='http://www.w3.org/1999/xhtml';
    me.vars=function(){
        // Var sandbox for wide use. Usage: ithz.uts.vars.<name> ; ithz.uts.vars.<name> = <value>
        var me={};return me;
        }();
    me.vars.errors=[];
    me.ns=ns;   // Namespace tool. Usage: ithz.uts.ns(<class tree string>); return created class
    me.$def=df; // Check if object has attribute with given name. Usage: ithz.uts.$def(<name string>,<object>); return boolean
    me.$=function(a,b){
        // Returns any DOM element with given id. Usage ithz.uts.$(<id string>); return DOM element
        if(!b){b=document;}
        return b.getElementById(a);
    };
    me.$tag=function(a,b){
        // Returns a list of DOM elements with given tagname. Usage: ithz.uts.$tag(<tagname string>); return HTML*Element list
        if(!b){b=document;}
        //if(me.$def("getElementsByTagNameNS",b)){return b.getElementsByTagNameNS(me.xmlns,a);}
        if(me.$def("getElementsByTagName",b)){return b.getElementsByTagName(a);}
        return null;
    };
    me.$css=function(a,b){
        // Get style rule with given id. Usage: uthz.uts.$css(<new or current rule id>); return object CSSStyleRule
        if(!b){b=document;}
        var s=b.styleSheets,fa="",al,m,i,il,r,j,jl,l,r,f;
        if(s){
            m=me.$def("cssRules",s[0])?0:me.$def("rules",s[0])?1:-1;
            if(m==0){
                al=a.split(",");
                for(i=0,il=al.length;i<il;i++){fa+=", "+me.trim(al[i]);}fa=fa.substring(2);
                for(i=0,il=s.length;i<il;i++){
                    r=s[i].cssRules;
                    if(r===null) continue;
                    for(j=0,jl=r.length;j<jl;j++){
                        if(r[j].selectorText==fa){return r[j];}
                    }
                }
                l=s[s.length-1];
                if(me.$def("insertRule",l)&&l.cssRules){return l.cssRules[l.insertRule(fa+' { }',l.cssRules.length)];}
            }else if(m==1){
                fa=me.trim(a.replace(/\"/g,"'"));
                for(i=0,il=s.length;i<il;i++){
                    r=s[i].rules;
                    for(j=0,jl=r.length,f=1;j<jl;j++){
                        if(r[j].selectorText.toLowerCase()==fa.toLowerCase()){return r[j];}
                    }
                }
                l=s[s.length-1];
                if(me.$def("addRule",l)){l.addRule(fa,null,-1);return l.rules[l.rules.length-1];}
            }
        }
        return null;
    };
    me.attr=function(o, a){
        // Get attribute of element
        var n="getAttribute", r=(o[n]&&o[n](a))||null, t=o.attributes;
        if(!r)
            for(var i=0,l=t.length;i<l;i++)
                if(t[i].nodeName===a)
                    return t[i].nodeValue;
        return r;
        };
    me.makeMap=function(str){
        // Creates a map-object from a csv string. Usage: ithz.uts.makeMap("csv,data,example")
        var o={},m=str.split(",");
        for(var i=0,il=m.length;i<il;i++){o[m[i]]=1;}
        return o;
        };
    me.redirect=function(u,d){
        // Redirects to given location after given delay, which defaults to zero,. Usage ithz.uts.redirect(<url>,<optional int ms delay>)
        var f=function(){self.location.href=u;};if(d||false){setTimeout(f,d);}else{f();}
    };
    me.nodeParents=function(a,b){
        // Get all nodes between a node and its parents given or root Usage: ithz.uts.nodeParents(<node>, <optional parent node>); return node array
        if(!b){b=null;}
        var n=a,r=[];
        while(n&&(n!=b)&&n.parentNode){
            r[r.length]=n;n=n.parentNode;
        }
        return r;
    };
    me.createNode=function(a,b){
        // Instantiate a new node of given type on current document. Usage: ithz.uts.createNode(<type string>); return node
        if(!b){b=document;}
        //if(me.$def("createElementNS",document)){return document.createElementNS(me.xmlns,a);}
        if(me.$def("createElement",b)){return b.createElement(a);}
        return null;
    };
    me.createTextNode=function(a,b){
        // Instantiate a new text node. Usage: ithz.uts.createNode(<text string>); return node
        if(!b){b=document;}
        return b.createTextNode(a);
    };
    me.insertBefore=function(m,o){
        // Insert node before given node. Usage: ithz.uts.inserBefore(<new element>,<reference element>)
        var p=o.parentNode;p.insertBefore(m,o);
    };
    me.insertAfter=function(m,o){
        // Insert node after given node. Usage: ithz.uts.inserAfter(<new element>,<reference element>)
        var p=o.parentNode,n=o.nextSibling;if(n){me.insertBefore(m,n);}else{p.appendChild(m);}
    };
    me.insertFirst=function(m,o){
        // Insert node as first child of given node. Usage: ithz.uts.inserFirst(<new element>,<reference element>)
        if(o.firstChild){me.insertBefore(m,o.firstChild);}
        else{o.appendChild(m);}
    };
    me.addEvent=function(o,ev,f,capture){
        // Add event to node. Usage: ithz.uts.addEvent(<node>,<event-name string>,<callback function>,<capture bool>)
        if(!me.$def("mev",o)){o.mev={};}
        if(!me.$def(ev,o.mev)){o.mev[ev]=[];}
        if(!me.$def("mevp",o)){o.mevp=1;}
        var v=o.mev[ev];
        v[v.length]=f;
        o.mevp&=(!capture);
        updateEvents(o,ev);
        return v.length-1;
    };
    me.popEvent=function(o,ev,id){
        // Pops event with id (returned by addEvent) from element. Usage: ithz.uts.popEvent(<node>,<event-name string>,<id>)
        if(!me.$def("mev",o)){return null;}else if(!me.$def(ev,o.mev)){return null;}
        var tr=o.mev[ev].splice(id,1);
        updateEvents(o,ev);
        return tr;
    };
    me.stopEvent=function(ev){
        // Capture event and stop its propagation. Usage: ithz.uts.stopEvent(<current event object>)
        var e=(!!ev)?ev:(me.$def("event"))?window.event:null;
        if(e){if(me.$def("stopPropagation",e)){e.stopPropagation();}e.cancelBubble=true;}
    };
    me.removeElement=function(o){o.parentNode.removeChild(o);}; // Remove element node. Usage: ithz.uts.removeElement(<node>)
    me.clearNode=function(o){
        // Remove element-node's content. Usage: ithz.uts.removeElement(<node>);
        if(o.childNodes){for(var i=0,l=o.childNodes.length;i<l;i++){o.removeChild(o.lastChild);}}
    };
    me.getDomain=function(s){
        // Get domain substring of given url. Usage: ithz.uts.getDomain(<url string>); return string
        return s.replace(/^(http:\/\/[^\/]+).*$/,"$1");
    };
    me.trim=function(s){
        // Return an string without start or tail spaces. Usage: ithz.uts.trim(<string>); return string
        return s.replace(/^\s+|\s+$/g,"");
    };
    me.permute=function(o){
        // Return all permutations of given array. Usage ithz.uts.permute(<array>); return array
        var t=[[o[0]]],i,il,j,jl,k,kl,c;
        for(i=1,il=o.length;i<il;i++){
            c=new Array();
            for(j=0,jl=t.length;j<jl;j++){
                for(k=0,kl=t[j].length+1;k<kl;k++){
                    c[c.length]=t[j].slice(0,k).concat(o[i],t[j].slice(k));
                }
            }
            t=c;
        }
        return t;
    };
    me.isEmpty=function(s){
        // Return true if string have anything but spaces, or false if doen't. Usage: ithz.uts.isEmpty(<string>); return bool
        return !!me.trim(s);
    };
    me.vars.pagedomain=me.getDomain(window.location+"");
    return me;
}();
ithz.nnm=function(){
    var me={};
    var jse=function(l,m){
        return {
            "loaded":(l)?!!l:false,
            "el":(m)?m:null
        };
    };
    var jsl={"page":new jse()},def=[],con=0,loa=0;

    var $def=ithz.uts.$def,$tag=ithz.uts.$tag;
    var checkLoaded=function(ids){
        for(var i=0,l=ids.length;i<l;i++){
            if(!jsl[ids[i]]||!jsl[ids[i]].loaded){return false;}
        }
        return true;
    };

    var dulock=false;
    var duqueue=function(){setTimeout(defUpdate,50);};
    var defUpdate=function(){
        if(dulock){duqueue();}
        else{
            dulock=true;
            var i=0;
            while(def[i]){
                if(checkLoaded(def[i][0])){def[i][1]();def.splice(i,1);}
                else{i++};
            }
            dulock=false;
        }
    };
    me.loaded=function(i){
        if($def(i,jsl)&&(!jsl[i].loaded)){
            jsl[i].loaded=true;
            defUpdate();
            loa++;
        }
    };
    me.path="";
    me.demmand=function(ids,func){
        me.deferExe(ids,func);
        me.add(ids);

    };
    me.add=function(ids){
        var i,l,k,el;
        if(typeof(ids)=="string"){ids=[ids];}
        for(i=0,l=ids.length;i<l;i++){
            k=ids[i];
            if(!$def(k,jsl)){
                el=ithz.uts.createNode("script");
                el.type="text/javascript";
                el.src=((me.path)?me.path+"/":"")+ids[i]+".js";
                jsl[k]=new jse(0,el);
                $tag("head")[0].appendChild(el);
                con++;
            }
        }
    };
    me.remove=function(id){
        var o=jsl[id];
        if(o&&o.el){ithz.uts.removeElement(o.el);delete jsl[id];}
    };
    me.deferExe=function(ids,func){
        if(checkLoaded(ids)){func();}
        else{def[def.length]=[ids,func];}
    };
    ithz.uts.addEvent(window,"load",function(){me.loaded("page");});
    return me;
}();
ithz.page={
    "top":function(){return (document.body.scrollTop||document.documentElement.scrollTop||0);},
    "width":function(){return (self.innerWidth||document.documentElement.clientWidth||0);},
    "height":function(){return (self.innerHeight||document.documentElement.clientHeight||0);},
    "theight":function(){
        var d=document,b=d.body,e=d.documentElement;
        return Math.max(Math.max(b.scrollHeight,e.scrollHeight),Math.max(b.clientHeight,e.clientHeight));
    },
    "twidth":function(){
        var d=document,b=d.body,e=d.documentElement;
        return Math.max(Math.max(b.scrollWidth,e.scrollWidth),Math.max(b.clientWidth,e.clientWidth));
    },
    "coords":function(o,a){
        var cl=0,ct=0,p=(a)?a:document.body;
        if(o.offsetParent){
            do{
                cl+=o.offsetLeft;
                ct+=o.offsetTop;
            }while((o.offsetParent!=p)&&(o=o.offsetParent));
        }
        return [cl,ct];
    }
};



