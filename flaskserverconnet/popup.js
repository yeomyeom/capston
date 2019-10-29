
window.addEventListener('load', function (evt) {
	chrome.extension.getBackgroundPage().chrome.tabs.executeScript(null, {
		file: 'payload.js'
	});
});

chrome.runtime.onMessage.addListener(function (message) {
	var serverurl = "http://127.0.0.1:5000";
	//serverurl = serverurl + message;
	chrome.tabs.create({url: serverurl});
	alert(message);
});

/*
chrome.runtime.onMessage.addListener(function (message) {
	document.getElementById('content').innerHTML = '스티커 ' + message + '개 제거했습니다.';
});*/