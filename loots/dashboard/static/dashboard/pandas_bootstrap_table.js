jQuery(function() {
  $('#datatable').DataTable( {
    "lengthMenu": [[25, 50, 100, -1], [25, 50, 100, "All"]],
    select: true
  } );
} );