$('#confirm-delete').on('show.bs.modal', function(e) {
    $(this).find('.btn-ok').attr('onclick', 'GetRefresh(' + $(e.relatedTarget).data('href') + ');');
    $('.debug-url').html('Delete Product: <strong>' + $(e.relatedTarget).attr('data-product')  + '</strong>');
});