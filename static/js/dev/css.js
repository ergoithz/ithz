ithz.css=function(){
    var me={};
    var $tag=ithz.uts.$tag,$def=ithz.uts.$def,$css=ithz.uts.$css;
    me.loadFile=function(src){
        var el=document.createElement("link");
        el.type="text/css";
        el.href=src;
        el.rel="StyleSheet";
        $tag("head")[0].appendChild(el);
    };
    var op=null;
    var opie=false;
    var l=["MozOpacity","KhtmlOpacity","opacity"];
    me.opacity=function(o,q){
		if (o===null) return;
        if (op===null){
            op=false;
            for(var i=0,n=l.length;i<n;i++){if($def(l[i],o.style)){op=l[i];break;}}
            if ((!op)&&($def("filter",o.style))){opie=true;}
        }
        if(q>0.9){q=1;}
        if(op){o.style[op]=q;}
        else if(opie){if(q>0.9){o.style.filter=null;}else{o.style.filter='alpha(opacity='+q*100+')';}}
    };
    var ra=null;
    var rap=[
        ["MozBorderRadius",function(o,tl,tr,br,bl){
            o.MozBorderRadiusTopleft=tl;o.MozBorderRadiusTopright=tr;o.MozBorderRadiusBottomright=br;o.MozBorderRadiusBottomleft=bl;
        }],
        ["webkitBorderRadius",function(o,tl,tr,br,bl){
            o.webkitBorderTopLeftRadius=tl;o.webkitBorderTopRightRadius=tr;o.webkitBorderBottomRightRadius=br;o.webkitBorderBottomLeftRadius=bl;
        }],
        ["borderRadius",function(o,tl,tr,br,bl){
            o.borderTopLeftRadius=tl;o.borderTopRightRadius=tr;o.borderBottomRightRadius=br;o.borderBottomLeftRadius=bl;
        }],
        [null,function(o,tl,tr,br,bl){return;}]
    ];
    me.radius=function(o,tl,xtr,xbr,xbl){
		if(o===null) return;
        var tr=(xtr===0)?"0":(xtr||tl),br=(xbr===0)?"0":(xbr||tl),bl=(xbl===0)?"0":(xbl||xtr||tl);
        var p=o.style,i,n;
        if (ra===null){
            n=rap.length;
            for(i=0;i<n;i++){if($def(rap[i][0],p)){ra=rap[i][1];break;}}
            if(ra===null){ra=function(a,b,c,d,e){};}
            }
        ra(p,tl,tr,br,bl);
    };
    me.jsreq=function(o){
        var d=o||document;
        if("\v"=="v"){
            $css(".jsrequired",d).style.display="inline";
            $css(".jsrequired",d).style.zoom="1";
        }else{
            $css(".jsrequired",d).style.display="inherit";
        }
        $css(".jsunrequired",d).style.display="none";
    };
    me.loadCSS=function(b){
        var i,il,toop,d=b||document;
        me.jsreq(d);
        if("\v"=="v"){
            toop=[".fakebtn_disabled","input[type=\"button\"][disabled=\"disabled\"]","button[disabled=\"disabled\"]"]; 
            for(i=0,il=toop.length;i<il;i++){
                me.opacity($css(toop[i],d),0.5);
            }
        }else{
            /* IE doesn't support multiple selectors or radius */
            me.radius($css(".dialogOuter",d),"12px");
            me.radius($css(".dialogContent",d),"10px");
            me.radius($css("input,.fakebtn,.fakebtn_active,.fakebtn_disabled,.inputcontainer,.textareacontainer",d),"3px");        
            me.radius($css(".select_replacer_clicked ul",d),"5px");
            me.radius($css(".select_replacer_clicked ul li",d),"2px");
            me.radius($css(".xhtml_textarea_codebuton_active",d),"3px","3px",0,0);
            me.opacity($css(".fakebtn_disabled,input[type=\"button\"][disabled=\"disabled\"],button[disabled=\"disabled\"]",d),0.5);
        }        
    };
    return me;
}();
ithz.nnm.deferExe(['css'],ithz.css.loadCSS);
ithz.nnm.loaded("css");
