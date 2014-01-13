$(function() {
    $('a#run').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_interpret', {
        statement: editor.getSession().getValue()
      }, function(data) {
        existing =  $("#console").text();
        existing += ">";
        existing += data.result + "\n";
        $("#console").text(existing);
      });
      return false;
    });
  });

$(function() {
    $('a#runDirect').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_interpretDirect', {
        statement: directWindow.getSession().getValue()
      }, function(data) {
        existing =  $("#console").text();
        existing += ">";
        existing += data.result + "\n";
        $("#console").text(existing);
      });
      return false;
    });
  });