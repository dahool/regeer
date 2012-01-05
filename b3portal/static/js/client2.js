$(document).ready(
	function() {
		// ajax boxes
		$('#client_aliases').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#client_aliases'));
		});
		$('#client_ipaliases').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#client_ipaliases'));
		});	
		$('#client_notice').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#client_notice'));
		});		
		$('#past_penalties').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#past_penalties'));
		});			
		$('#admin_actions').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#admin_actions'));
		});
		$('#portal_actions').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#portal_actions'));
		});			
	}
);