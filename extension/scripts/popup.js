$(function(){

    
    $('#keywordsubmit').click(function(){

		console.log("hello");
		
		//var search_topic = $('#keyword').val();
		
		var model = $('#models').val();
		console.log(model);
		
		chrome.tabs.query({

			active: true,
			currentWindow: true

		}, function(tabs) {

			var tabURL = tabs[0].url;
			

		
            chrome.runtime.sendMessage(

					{active_url: tabURL,
					model_chosen: model},

					function(response) {
						result = response.farewell;
						alert(result.language);

						console.log(result.language);
						
				});
		
		});
			
			
		$('#keyword').val('');
		
    });
});