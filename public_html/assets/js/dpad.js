(function ($) {
  var sendAction = function(a) {
    $.get('http://' + window.location.hostname + ':61338/api', {
        action: a
    }, function (data) {

    });
  };


  $("#video_feed").attr("src", "http://" + window.location.hostname + ":5000/");

  sendAction("PP");
  sendAction("PS");

  $(window).keydown(function(key) {
    if( key.keyCode === 32 ) sendAction("PSPACE");
    if( key.keyCode === 37 ) sendAction("PLEFT");
    if( key.keyCode === 38 ) sendAction("PUP");
    if( key.keyCode === 39 ) sendAction("PRIGHT");
    if( key.keyCode === 40 ) sendAction("PDOWN");
    if( key.keyCode === 72 ) sendAction("PD");
  });
  $(window).keyup(function(key) {
    if( key.keyCode === 37 ) sendAction("RLEFT");
    if( key.keyCode === 38 ) sendAction("RUP");
    if( key.keyCode === 39 ) sendAction("RRIGHT");
    if( key.keyCode === 40 ) sendAction("RDOWN");
  });

  $("#btnDown").mousedown(function () {
    $(this).effect("highlight", { color: "#ffffff" }, 100);
    sendAction("PDOWN");
  });
  $("#btnLeft").mousedown(function () {
    $(this).effect("highlight", { color: "#ffffff" }, 100);
    sendAction("PLEFT");
  });
  $("#btnRight").mousedown(function () {
    $(this).effect("highlight", { color: "#ffffff" }, 100);
    sendAction("PRIGHT");
  });
  $("#btnUp").mousedown(function () {
    $(this).effect("highlight", { color: "#ffffff" }, 100);
    sendAction("PUP");
  });

  $("#btnHorn").click(function () {
    $(this).effect("highlight", { color: "#ffffff" }, 100);
    sendAction("PSPACE");
  });
  $("#btnHome").click(function () {
    $(this).effect("highlight", { color: "#ffffff" }, 100);
    sendAction("PD");
  });

  $("#btnDown").mouseup(function () {
    sendAction("RDOWN");
  });
  $("#btnLeft").mouseup(function () {
    sendAction("RLEFT");
  });
  $("#btnRight").mouseup(function () {
    sendAction("RRIGHT");
  });
  $("#btnUp").mouseup(function () {
    sendAction("RUP");
  });
})(jQuery);
