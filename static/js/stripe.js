/**
 * JS to apply the Stripe API
 *
 * @author    Dave Widmer
 */
Stripe.setPublishableKey('pk_CWozmASNiTiIpSDNF9Q68JtvvEzRl');
var form = $("#payment-form");

$(document).ready(function() {
	form.submit(function(event) {
		// disable the submit button to prevent repeated clicks
		$('.submit-button').attr("disabled", "disabled");

		Stripe.createToken({
			number: $('#card-number').val(),
			cvc: $('#card-cvc').val(),
			exp_month: $('#card-expiry-month').val(),
			exp_year: $('#card-expiry-year').val()
		}, stripeResponseHandler);

		// prevent the form from submitting with the default action
		return false;
	});
});

function stripeResponseHandler(status, response) {
    if (response.error) {
        $("#payment-errors").text(response.error.message).show();
    } else {
        var token = response['id'];
        // insert the token into the form so it gets submitted to the server
        form.append("<input type='hidden' name='stripeToken' value='" + token + "'/>");
        // and submit
        form[0].submit();
    }
}