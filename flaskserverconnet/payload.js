var currenturl = location.href;
var changeurl = '';
if(currenturl.indexOf("blog.naver.com") != -1){
    var mainFrame = document.getElementsByName('mainFrame');
    if(mainFrame[0] != null){
        var innerHtmlUrl = mainFrame[0].src;
        location.href = innerHtmlUrl;
    }
    else{
        currenturl = currenturl.split('?')[1];
        changeurl += currenturl.split('&')[0];
        changeurl += '&';
        changeurl += currenturl.split('&')[1];
        sendingMeg = JSON.parse(JSON.stringify(changeurl));
        chrome.runtime.sendMessage(sendingMeg);
    }
}
else{
    var frameset = document.getElementsByName('screenFrame');
    if(frameset[0]!=null){
        var blogUrl = frameset[0].src;
        location.href = blogUrl;
    }
}