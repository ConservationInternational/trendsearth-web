$(document).ready(function () {});

var showMessage = function (msg, error_type = "success") {
  $(window).scrollTop(0);
  let panel = $("#messages-panel");
  panel.empty();
  panel.append(`
  <div class="alert m-2 alert-${error_type}" id="msg" role="alert">
    ${msg}
  </div>`);
  setTimeout(function () {
    panel.empty();
  }, 4000);
};
