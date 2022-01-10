var serverhost = 'http://0.0.0.0:5000';

	chrome.runtime.onMessage.addListener(
		function(request, sender, sendResponse) {

			var url = serverhost + '/detect/string?url='+ encodeURIComponent(request.active_url) + '&model='+encodeURIComponent(request.model_chosen);
			
			console.log(url);
			
			fetch(url)
			.then(response => response.json())
			.then(response => sendResponse({farewell: response}))
			.catch(error => console.log(error))
				
			return true;  // Will respond asynchronously.
	});
