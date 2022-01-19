$(document).ready(function () {});

const showMessage = function (msg, timeout) {
  $("#messages-list").removeClass("msg-white");
  $("#messages-list").addClass("msg-dark");
  const messages = document.getElementById("messages-list");
  messages.innerHTML = msg;

  $("#messages-list").fadeOut(timeout, "swing", function () {
    messages.innerHTML = "";
    $("#messages-list").show();
    $("#messages-list").removeClass("msg-black");
    $("#messages-list").addClass("msg-white");
  });
};
