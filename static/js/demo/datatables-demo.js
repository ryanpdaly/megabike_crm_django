// Call the dataTables jQuery plugin
$(document).ready(function() {
  var myTable = $('#dataTable').DataTable({
  	"processing": true,
  	"serverSide": true,
  	"ajax": "{% url 'customers:customer-list' %}",

  });
});
