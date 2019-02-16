# -*- coding: utf-8 -*-
class Const:
    
    # 크롤링 사이트 요소(element) 추출을 위한 코드
    HTML_BODY_PREFIX = "<html><body>"
    HTML_BODY_SUFFIX = "</body></html>"
    # EXTRA_SCRIPT_CODE = "<script>(function(){var s=document.createElement('div');s.innerHTML='Loading...';s.style.color='black';s.style.padding='20px';s.style.position='fixed';s.style.zIndex='9999';s.style.fontSize='3.0em';s.style.border='2px%20solid%20black';s.style.right='40px';s.style.top='40px';s.setAttribute('class','selector_gadget_loading');s.style.background='white';document.body.appendChild(s);s=document.createElement('script');s.setAttribute('type','text/javascript');s.setAttribute('src','http://www.pparisa.com/lib/ext/gadget/selectorgadget_custom.js');document.body.appendChild(s);})();</script>"
    EXTRA_SCRIPT_CODE = '''
        <script>
        ( function(){
            var s=document.createElement('div');
            s.innerHTML='Loading...';
            s.style.color='black';
            s.style.padding='20px';
            s.style.position='fixed';
            s.style.zIndex='9999';
            s.style.fontSize='3.0em';
            s.style.border='2px%20solid%20black';
            s.style.right='40px';
            s.style.top='40px';
            s.setAttribute('class','selector_gadget_loading');
            s.style.background='white';
            document.body.appendChild(s);
            s=document.createElement('script');
            s.setAttribute('type','text/javascript');
            s.setAttribute('src','http://www.pparisa.com/lib/ext/gadget/selectorgadget_custom.js');
            document.body.appendChild(s);
        })();
        </script>
    '''

    # AJAX 후킹
    AJAX_HOOKING_SCRIPT_CODE = '''
        <script src="https://code.jquery.com/jquery-2.2.4.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.js"></script>
        <script>
        ( function(){ 
            
            console.log("ajax hooking");                  
                  
            $( document ).ajaxSend( function( evt, request, settings ) {
            
                // queryString
                var qs = (function(a) {
                    if (a == "") return {};
                    var b = {};
                    for (var i = 0; i < a.length; ++i)
                    {
                        var p=a[i].split('=', 2);
                        if (p.length == 1)
                            b[p[0]] = "";
                        else
                            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
                    }
                    return b;
                })(window.location.search.substr(1).split('&'));
            
                var PREFIX_ORIG_URL = "?url=";
                var targetUrl = evt.target.URL; // ㅅ
                
                console.log("[1] Target URL = ", targetUrl );
                console.log("[2] Origin Path = ", settings.url );
                console.log("[3] Origin Data = ", settings.data );
                                
                var index = targetUrl.indexOf( PREFIX_ORIG_URL );
                var originUrl = targetUrl.substring( index + PREFIX_ORIG_URL.length, targetUrl.length );                
                settings.url = "/proxyAjax?orig_url=" + originUrl + "&orig_path=" + settings.url;
            });                                                                   
            
        }) ();
        </script>
    '''