
window.addEventListener('load', function (evt) {
	chrome.extension.getBackgroundPage().chrome.tabs.executeScript(null, {
		file: 'payload.js'
	});
});

chrome.runtime.onMessage.addListener(function (message) {
	var serverurl = "http://127.0.0.1:5001/";
	serverurl = serverurl + message;
	alert(message);
	chrome.tabs.create({url: serverurl});
	
	//ajax_post();
});

/*
function ajax_post(){
	$.ajax({
		type: "POST",
		url: "http://127.0.0.1:5000/",
		//url: "http://54.180.103.78:8000/analysis/",
		data: {
			'url': url,
			'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
		},
		success: Success,
		dataType: 'json'
	});

};
*/
/*
chrome.runtime.onMessage.addListener(function (message) {
	document.getElementById('content').innerHTML = '스티커 ' + message + '개 제거했습니다.';
});*/