$(function() {
  $('a.delete').click(function() {
    if (confirm("Are you sure?")) {
      document.location.href = $(this).attr('href');
    }
    return false;
  });
});