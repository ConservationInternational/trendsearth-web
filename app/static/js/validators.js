$(document).ready(function () {
  /*****
   *  Input validators
   *
   * */
  $(`input[required=true], select[required=true]`).on("keyup", function () {
    if ($(this).is(":visible")) {
      $(this).removeClass("invalid");
      $(this).css("border-color", "#aaaaaa");
      $(this).css("background-color", "#ffffff");
      if ($(this).val() == "" || $(this).val() == null) {
        $(this).addClass("invalid");
        $(this).css("border-color", "red");
        $(this).css("background-color", "#ffdddd");
      }
    }
  });

  $(`select[required=true]`).on("change", function () {
    if ($(this).is(":visible")) {
      $(this).removeClass("invalid");
      $(this).css("border-color", "#aaaaaa");
      $(this).css("background-color", "#ffffff");
      if ($(this).val() == "" || $(this).val() == null) {
        $(this).addClass("invalid");
        $(this).css("border-color", "red");
        $(this).css("background-color", "#ffdddd");
      }
    }
  });

  /****/
});
const validate_form = function (n, currentTab) {
  /**
   * Validate scheme loggement form
   * n : form ID
   * currentTab: index of the current tab
   */
  var valid = true;
  $(
    `#lodgementForm${n} input[required=true], #lodgementForm${n} select[required=true]`
  ).each(function () {
    if ($(this).is(":visible")) {
      $(this).removeClass("invalid");
      $(this).css("border-color", "#aaaaaa");
      $(this).css("background-color", "#ffffff");
      if ($(this).val() == "" || $(this).val() == null) {
        $(this).addClass("invalid");
        valid = false;
        $(this).css("border-color", "red");
        $(this).css("background-color", "#ffdddd");
      }
    }
  });

  var counter = 0;
  $(`#lodgementForm${n} a:visible`).each(function () {
    if ($(this).attr("href") === "" || $(this).attr("href") === "#") {
      valid = false;
    } else {
      counter += 1;
    }
  });

  if (n == 3) {
    var rowcount = $(`#holders_tbl >tbody:last > tr`).length;
    if (counter <= rowcount) {
      valid = true;
      $("#file-holders").removeClass("invalid");
      $("#file-holders").css("border-color", "#aaaaaa");
      $("#file-holders").css("background-color", "#ffffff");
    }
    if ($("#inputValidationResult").find("li").length > 1 && rowcount < 1)
      valid = false;
  }

  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid;
};
