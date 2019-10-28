
window.addEventListener('load', function (evt) {
	chrome.extension.getBackgroundPage().chrome.tabs.executeScript(null, {
		file: 'payload.js'
	});
});

/*
window.addEventListener('load', function (evt) {
	file: 'payload.js'
	chrome.tabs.create({url: "http://127.0.0.1:5000"});
});
*/
chrome.runtime.onMessage.addListener(function (message) {
	chrome.tabs.create({url: "http://127.0.0.1:5000"});
	alert(message);
});

/*
chrome.runtime.onMessage.addListener(function (message) {
	document.getElementById('content').innerHTML = '스티커 ' + message + '개 제거했습니다.';
});*/