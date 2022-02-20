const validateMatrixTable = function () {
  $(".lc-input").on("keyup", function () {
    var inputVal = $(this).val();
    if (inputVal.length > 1) {
      inputVal = inputVal[0];
      $(this).val(inputVal);
    }
    if (!/[-0+]/.test(inputVal)) {
      $(this).val("");
    } else {
      $(this).removeClass("stable");
      $(this).removeClass("degradation");
      $(this).removeClass("improvement");

      if (inputVal == "0") {
        $(this).addClass("stable");
      } else if (inputVal == "-") {
        $(this).addClass("degradation");
      } else {
        $(this).addClass("improvement");
      }
    }
  });
};
