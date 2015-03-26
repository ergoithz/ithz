ithz.ctl.xtr=function(){
    var me={};
    var addev=ithz.uts.addEvent,popev=ithz.uts.popEvent,
        $tag=ithz.uts.$tag,
        $def=ithz.uts.$def,addnode=ithz.uts.createNode,
        addtext=ithz.uts.createTextNode,clearNode=ithz.uts.clearNode,
        insertAfter=ithz.uts.insertAfter,insertBefore=ithz.uts.insertBefore;
    var rtclass="xhtml_textarea";
    var rticlass="xhtml_textarea_iframe";
    var rtibclass="xhtml_textarea_iframe_body";
    var rttclass="xhtml_textarea_topbar";
    var rtcaclass="xhtml_textarea_codebuton_active";
    var rtsclass="xhtml_textarea_statusbar";
    var rtscclass="xhtml_textarea_statusbar_caret";
    var rtssclass="xhtml_textarea_statusbar_status";
    var rtdsi="xhtml_textarea_select_iframe";
    var rtih="<link rel=\"StyleSheet\" type=\"text/css\" href=\"/style/fixes/reset.css\"/><link rel=\"StyleSheet\" type=\"text/css\" href=\"/style/content.css\"/><style type=\"text/css\">body{background:#EBF3D1;}</style>";
    var appendTemporallyChild=function(n,o,t){
        o.appendChild(n);setTimeout(function(){ithz.uts.removeElement(n);},(t||5000));
    };
    var xr={"<b>":"<strong>","</b>":"</strong>","<i>":"<em>","</i>":"</em>"};
    var xml=function(r,o){
        try{
            var tr=ithz.rhp.HTMLtoXML(o);
            for(var i in xr){tr=tr.replace(new RegExp(i,"ig"),xr[i]);}
            return tr;
        }catch(ec){
            var msg=ec.toString();
            if(msg.toLowerCase().indexOf("parse error")>-1){
                msg="Wrong xHTML syntax ignored ("+msg+").";
            }
            appendTemporallyChild(addtext(msg),r.r.sts,5000);
            return null;
        }
    };
    var addCodeTo=function(st,dc){
        var pf=function(r,btn){
            var f=function(e){
                ithz.uts.stopEvent(e);
                if(!btn.disabled){
                    var cs,ce,sel,sel2,rp,pc,doc=r.r.pv.gdoc();
                    if((!e)&&($def("event"))){e=window.event;}
                    if((r.r.m)&&(dc)){
                        r.r.pv.sfocus();
                        if(r.r.pv.allow(dc[0])){r.r.pv.exec(dc[0],(dc[1]||""));}
                        else{doc.body.innerHTML=st[0]+(st[1]||"")+doc.body.innerHTML;}
                            
                    }else if(st){
                        cs=r.r.carets;
                        ce=r.r.carete;
                        rp=false;
                        sel=r.value.substring(cs,ce);
                        pc=sel.search(st[0]);
                        if(pc>-1){
                            sel2=sel.substring(pc+st[0].length);
                            if(sel2.search(st[1])>-1){
                                rp=true;
                                sel=sel.substring(0,pc)+sel2.replace(st[1],"");
                            }
                        }
                        if(!rp){
                            sel=st[0]+sel+(st[1]||"");
                        }
                        if($def("selectionStart",r)){
                            r.value=r.value.substring(0,cs)+sel+r.value.substring(ce);
                            r.selectionStart=cs;
                            r.selectionEnd=cs+sel.length;
                        }else if($def("selection",doc)){
                            doc.selection.createRange().text=sel;
                        }
                        r.focus();           
                    }
                }
                return false;
            };
            f.btn=btn;
            f.internal=false;
            f.html=!!(st&&st.length);
            f.dc=dc;
            return f;
        };
        return pf;
    };
    var synchronize=function(r){
        var w=xml(r,r.r.pv.gdoc().body.innerHTML);
        if(w!=r.r.pv.base){r.value=w;return true;}
        return false;
    };
    var toggleMode=function(r,btn){
        var f=function(e){
            ithz.uts.stopEvent(e);
            var w,a,d,i,il,bb,css;
            if((!e)&&($def("event"))){e=window.event;}
            if(r.r.m){
                r.r.m=0;
                bb=r.r.bb;
                synchronize(r);
                r.style.display="block";
                r.r.pv.style.display="none";
                r.r.pvb.className=rtcaclass;
                
                r.focus();
                for(i=0,il=bb.length;i<il;i++){
                    d=(!bb[i].internal)&&(!bb[i].html);
                    bb[i].btn.disabled=d;
                    if(bb[i].btn.className!=rtcaclass){
                        bb[i].btn.className=(d?"fakebtn_disabled":"fakebtn");
                    }
                }
            }else{
                r.r.m=1;
                w=r.r.pv.gdoc();
                clearNode(r.r.stc);
                a=xml(r,r.value);
                if(a!==null){
                    r.r.pv.stoggle(false);
                    w.open();
                    w.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?\\><"+"!"+"DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\"><head><title>Edit<"+"/title>"+rtih+"<"+"/head><body class=\"content\">"+a+"<"+"/body><"+"/html>");
                    w.close();
                    r.r.pv.base=a;
                }
                r.r.pv.stoggle(true);
                r.r.pv.style.display="block";
                r.style.display="none";
                r.r.pv.loadedFocus();
                r.r.pvb.className="fakebtn";
                
            }
            return false;
        };
        f.btn=btn;
        f.internal=true;
        f.html=true;
        f.dc=[];
        return f;
    };
    var addImage=function(r,btn){
        var ev=null;
        var f=function(e){
            ithz.nnm.demmand(["ufr","sir"],function(){
                var ff=addnode("fieldset"),le=addnode("legend"),i1=addnode("ol"),i2=addnode("ol"),we1=-1,we2=-1,html;
                ff.className="formFieldset";
                ff.style.display="block";
                le.appendChild(addtext("Select image"));
                ff.appendChild(le);ff.appendChild(i1);ff.appendChild(i2);
                i1.r={};i2.r={"hfix":50};
                
                r.r.dialog.realize();
                
                ithz.ctl.ufr.ruform(i1);
                ithz.ctl.sir.replace(i2,true,r.r.dialog.outer);
                
                var fload=1; // Don't refresh but relocate on first load
                addev(i1.r,"load",
                    function(){
                        i2.r.relocate();
                        if(!fload){
                            i2.r.refresh();
                        }else{
                            fload=0;
                        }
                    });
                addev(i1.r,"load",r.r.dialog.relocate);
                addev(i2.r,"load",i2.r.relocate);
                addev(i2.r,"load",r.r.dialog.relocate);
                
                we1=addev(window,"resize",i2.r.relocate);
                we2=addev(window,"resize",r.r.dialog.relocate);
                              
                r.r.dialog.hid=addev(r.r.dialog,"hide",function(e){
                    r.r.dialog.unrealize();
                    popev(window,"resize",we1);
                    popev(window,"resize",we2);
                    popev(r.r.dialog,"hide",r.r.dialog.hid);
                });
                addev(i2,"select",function(e){
                    r.r.dialog.hide();
                    r.r.pv.sfocus();
                    html="<img src=\""+e.href+"\" alt=\"\"/>";
                    addCodeTo([html],["inserthtml",html])(r,btn)(ev);
                });
                r.r.dialog.pack(ff);
                r.r.dialog.style.width="600px";
                r.r.dialog.show();
            });
            return false;
        };
        f.btn=btn;
        f.internal=true;
        f.dc=[];
        return f;
    };
    var updateStatus=function(r){
        var stc=r.r.stc;
        if(r.r.m){
            var i,il=0,bb=r.r.bb,l,d,pv=r.r.pv,nn,node,w=r.r.pv.contentWindow;
            clearNode(stc);
            /*
            if($def("getSelection",w)){
                var range=r.r.pv.contentWindow.getSelection().getRangeAt(0);
            }

            l=ithz.uts.nodeParents(e.target,r.r.pv.gdoc().body);
            for(i=0,il=l.length;i<il;i++){
                nn=l[i].nodeName.toLowerCase();
                if((nn=="html")||(nn=="body")){il=0;break;}
                node=addnode("span");
                node.className="dompath";
                node.appendChild(addtext(nn+((l[i].id)?"#"+l[i].id:"")));
                ithz.uts.insertFirst(node,sts);
                if(i<il-1){
                    node=addnode("span");
                    node.className="dompathsep";
                    node.appendChild(addtext(">"));
                    ithz.uts.insertFirst(node,sts);
                }
            }
            
            if(il===0){
                node=addnode("span");
                node.className="dompath";
                node.appendChild(addtext("\\"));
                ithz.uts.insertFirst(node,sts);
            }
            */
            // BDS
            for(i=0,il=bb.length;i<il;i++){
                d=!bb[i].internal;
                if(d&&pv&&bb[i].dc[0]){
                    d=!r.r.pv.allow(bb[i].dc[0]);
                }
                bb[i].btn.disabled=d;
                if(bb[i].btn.className!=rtcaclass){
                    bb[i].btn.className=(d?"fakebtn_disabled":"fakebtn");
                }
            }
        }else{
            var cs=0,ce=0,s,ds,n,eol;
            if(r.selectionStart){
                cs=r.selectionStart;
                ce=r.selectionEnd;
            }else if(("\v"=="v")&&(document.selection)){
                var jojo=document.selection.length;
                s=document.body.createTextRange();
                s.moveToElementText(r);
                ds=document.selection.createRange();
                while(s.compareEndPoints("StartToStart",ds)<0){s.moveStart("Character",1);cs++;}
                ce=cs+jojo;
            }
            r.r.carets=cs;
            r.r.carete=ce;
            clearNode(stc);
            n=r.value.substring(0,cs);
            eol=n.lastIndexOf("\n");
            stc.appendChild(addtext("Line "+(n.replace(/[^\n]/g, "").length+1)+", col "+n.substring(eol?eol+1:0).length+" (char "+cs+")"));    
        }
    };
    var iconpath="/icons/";
    //Text, image, action
    var xtb=[
        ["Undo",iconpath+"arrow_undo.png",addCodeTo(null,["undo"])],
        ["Redo",iconpath+"arrow_redo.png",addCodeTo(null,["redo"])],
        ["Bold",iconpath+"text_bold.png",addCodeTo(["<strong>","</strong>"],["bold"])], 
        ["Text to italic",iconpath+"text_italic.png",addCodeTo(["<em>","</em>"],["italic"])],
        ["Underline text",iconpath+"text_underline.png",addCodeTo(["<span style=\"text-decoration:underline\">","</span>"],["underline"])],
        ["Strike text",iconpath+"text_strikethrough.png",addCodeTo(["<strike>","</strike>"],["strikethrough"])],
        ["Align to left",iconpath+"text_align_left.png",addCodeTo(["<p style=\"text-align:left\">","</p>"],["justifyleft"])],
        ["Align to center",iconpath+"text_align_center.png",addCodeTo(["<p style=\"text-align:center\">","</p>"],["justifycenter"])],
        ["Align to right",iconpath+"text_align_right.png",addCodeTo(["<p style=\"text-align:right\">","</p>"],["justifyright"])],
        ["Unordered list",iconpath+"text_list_bullets.png",addCodeTo(["<ul><li>","</li></ul>"],["insertunorderedlist"])],
        ["Ordered list",iconpath+"text_list_numbers.png",addCodeTo(["<ol><li>","</li></ol>"],["insertorderedlist"])],
        ["Add image",iconpath+"image-x-generic.png",addImage],
        ["Page code",iconpath+"xhtml.png",toggleMode]
        ];
    var xe=[[">","&gt;"],["<","&lt;"],["&","&amp;"],["\"","&quot;"],["'","&apos;"]];
    me.rta=function(r){
        var i,m,il,cmd,sync,pv=addnode("iframe"),tb=addnode("div"),st=addnode("div"),stc=addnode("div"),sts=addnode("div"),hr=addnode("hr");
        pv.gdoc=function(){return (pv.contentDocument||pv.contentWindow.document||pv.document);};
        pv.gwin=function(){return (pv.contentWindow||pv);};
        pv.exec=function(cmd,param){pv.gdoc().execCommand(cmd,false,(param)?param:null);};
        pv.stoggle=function(o){var a="styleWithCSS";pv.gdoc().designMode=(o?"on":"off");if(pv.allow(a)){pv.exec(a,"false");}};
        pv.sfocus=function(){
            var f=pv,cw=pv.gwin(),doc=pv.gdoc();
            if($def("focus",f)){f.focus();}
            if($def("focus",cw)){cw.focus();}
            if($def("focus",doc)){doc.focus();}
            };
        pv.loadedFocus=function(){
            if($def("elid",pv)){ithz.uts.popEvent(pv,"load",pv.elid);}
            pv.elid=addev(pv,"load",pv.sfocus);
            };
        pv.allow=function(cmd){
            var tr=false,doc=pv.gdoc();
            if($def("queryCommandEnabled",doc)){try{tr=doc.queryCommandEnabled(cmd);}catch(e){void(0);}}
            return tr;
            };
        r.r.carets=0;
        r.r.carete=0;
        r.r.pv=pv;
        r.r.sts=sts;   
        r.r.stc=stc;
        r.r.dialog=ithz.ctl.fpr.dialog();
        if(!r.className){r.className=rtclass;}
        pv.className=rticlass;
        tb.className=rttclass;
        st.className=rtsclass;
        sts.className=rtssclass;
        stc.className=rtscclass;
        hr.className="hr";
        r.r.bb=[];
        for(i=0,il=xtb.length;i<il;i++){
            m=addnode("img");
            m.className="fakebtn";
            m.alt=xtb[i][0];
            m.src=xtb[i][1];
            m.style.width="16px";
            m.style.height="16px";
            cmd=function(i,r,m){return xtb[i][2](r,m);}(i,r,m);
            addev(m,"mousedown",function(m){return function(){if(!m.disabled){m.className="fakebtn_active";}};}(m));
            addev(m,"mouseup",function(m){return function(){if(!m.disabled){m.className="fakebtn";}else{m.className="fakebtn_disabled";}};}(m));
            addev(m,"click",cmd);
            tb.appendChild(m);
            r.r.bb[r.r.bb.length]=cmd;
            }
        r.r.pvb=tb.lastChild;
        st.appendChild(sts);st.appendChild(stc);
        insertAfter(hr,r);insertAfter(st,r);insertAfter(pv,r);
        insertBefore(tb,r);
        pv.style.display="none";
        var done=false;
        sync=function(){
            if(!done){
                done=true;
                var v=0;
                if(r.r.m){v=synchronize(r);}
                if(!v){var a=xml(r,r.value);if(a!=null){r.value=a;}}
                }            
            };
        if($def("ajx",ithz)){ithz.ajx.addCallback("action",sync,true);}
        else{addev(r.form,"submit",sync);}
        
        if($def("chrome")||$def("opera")){
            // Chrome & Opera workaround
            var sb=0,t,te={"text":1,"password":1},tc={"submit":1,"image":1},enter=function(e){
                var k=($def("event"))?window.event.keyCode:e.which;
                if(k==13){sync();}
                };
            if(t=$tag("input",r.form)){
                for(i=0,il=t.length;i<il;i++){
                    if(t[i].type in tc){addev(t[i],"click",sync);}
                    if(t[i].type in te){addev(t[i],"keypress",enter);}
                    }
                }
            }
        r.r.usi=setInterval(function(){
            if(ithz.uts.$(r.id)!=r){clearInterval(r.r.usi);}
            else{updateStatus(r);}          
            },1000);
        (toggleMode(r,r.r.pvb))(null);
        };
    return me;
    }();
ithz.nnm.loaded("xtr");
