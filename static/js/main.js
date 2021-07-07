const user_input = $("#user-input")
const search_icon = $("#search-icon")
const customers_div = $("#replaceble-content")
const endpoint = 'warranty/new/'
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
	$.getJSON(endpoint, request_parameters)
		.done(response => {
				// fade out customers_div, then:
				$("#replaceable-content").fadeTo('slow', 0).promise().then(() =>{
					// replace the HTML contents
					$("#replaceable-content").html(response['html_from_view'])
					// fade-in the div with new contents
					$("#replaceable-content").fadeTo('slow', 1)
					// stop animating search icon; Doesn't seem to work so far?
					$("#search-icon").removeClass('blink')
				})
			})
		.fail(function() {
			console.log("Ajax failed")
	})
};

$("#user-input").keyup(function() {
	const request_parameters = {
		kdnr_input: $(this).val(), // value of user_input: HTML element with ID user-input
		kdnr_checked: $("input[name='customerRadios']:checked").val()
	}

	// start animating the search icon with CSS class
	search_icon.addClass('blink')

	// if scheduled_function is NOT false, cancel execution of the function
	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	// setTimeout returns the ID of function to be executed
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
});

$("#replaceable-content").on("change", "input[name='customerRadios']", function(event){
	const request_parameters = {
		kdnr_input: $("#user-input").val(),
		kdnr_checked: $("input[name='customerRadios']:checked").val()
	}

	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)

});