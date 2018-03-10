$(document).ready(function() {
	
    $("#test").html("Test!"); 

	$("#NQ").keydown(function(e) {
        if(e.which == 13) {
            this.form.submit();
        }
	});
	
	
	//Changes color of upvote and rating number when clicked
	$(".ratingArea").find("#voteUp").click(function(e) {
		rateDiv = $(this).closest("div");
		downBtn = rateDiv.find("#voteDown");
		
		rateEl = rateDiv.find("#rating")
		curRate = parseInt(rateEl.html());
		if (downBtn.hasClass('votedDown')){
			rateEl.html(curRate+2);
		}
		else if (!($(this).hasClass('votedUp')) && !(downBtn.hasClass('votedDown'))){
			rateEl.html(curRate+1);
		}
		
		downBtn.removeClass('votedDown');
		$(this).addClass('votedUp');
		
	});
	
	//Changes color of downvote and rating number when clicked
	$(".ratingArea").find("#voteDown").click(function(e) {
		rateDiv = $(this).closest("div");
		upBtn = rateDiv.find("#voteUp");
		
		rateEl = rateDiv.find("#rating")
		curRate = parseInt(rateEl.html());
		if (upBtn.hasClass('votedUp')){
			rateEl.html(curRate-2);
		}
		else if (!($(this).hasClass('votedDown')) && !(upBtn.hasClass('votedUp'))){
			rateEl.html(curRate-1);
		}
		
		upBtn.removeClass('votedUp');
		$(this).addClass('votedDown');
	});
	
/*	$('#submit').click(function(){ */
	$('#inp').keydown(function(e) {
		if(e.which == 13) {
			
			$("#inp").prop("readonly", true);
			
			var input = $('input#inp').val();
			$('#inp').val('');
			var history = $('#CWindow').html();	
			$('#CWindow').html(history + '<div class="msgContainer" align="right"><p>' + input + '</p><br><div class="msgLabel">You</div></div>');
			function loadGif() {
				$('#CWindow').html(history + '<div class="msgContainer" align="right"><p>' + input + '</p><br><div class="msgLabel">You</div></div>' + '<div class="botmsgContainer"><img src="http://www.witchdoctorcomic.com/wp-content/plugins/funny-chat-bot/images/load.gif" style="max-height: 50px; max-width: 50px;" /></div>');
				div = $('#CWindow');
				div.scrollTop(div.prop('scrollHeight'))
			}
			function grabAnswer() {
				$.get('/chatAnswer/', {"question": input}, function(data) {	
					$('#CWindow').html(history + '<div class="msgContainer" align="right"><p>' + input + '</p><br><div class="msgLabel">You</div></div>' + '<div class="botmsgContainer"><p >' + data + '</p><br><div class="msgBotLabel">Chatbot</div></div>');			
					div = $('#CWindow');
					div.scrollTop(div.prop('scrollHeight'))
					$("#inp").prop("readonly", false);
				});			
			}
			setTimeout(loadGif, 500);
			setTimeout(grabAnswer, 1000);
			
			div = $('#CWindow');
			div.scrollTop(div.prop('scrollHeight'))
		}
	});
});

// Hide or show account drop down
function profileFunc() {
    document.getElementById("profileDropdown").classList.toggle("show");
}

//Ajax call to voting function and changes rating number on page
function vote(elem, rating, answerID, userID) { 
	$.get('/voting/', {"rating": rating, "answer": answerID, "user": userID}, function(data) {		
//		rateDiv = $(elem).closest("div");
//		rating = rateDiv.find("#rating");
//		rating.html(data);
	});	
}

// Close the account drop down when click is made outside of content
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var accElements = document.getElementsByClassName("profile-content");
    var i;
    
    for (i = 0; i < accElements.length; i++) {
      var elem = accElements[i];
      if (elem.classList.contains('show')) {
    	  elem.classList.remove('show');
      }
    }
  }
}
