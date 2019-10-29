var currenturl = location.href;

if(currenturl.indexOf("blog.naver.com") != -1){
    var mainFrame = document.getElementsByName('mainFrame');
    if(mainFrame[0] != null){
        var innerHtmlUrl = mainFrame[0].src;
        location.href = innerHtmlUrl;
    }
    else{
        sendingMeg = JSON.parse(JSON.stringify(currenturl));
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