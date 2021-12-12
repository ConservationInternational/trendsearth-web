const fixStepIndicator = function (n) {
  var i,
    x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  x[n].className += " active";
};

const nextPrev = function (n, currentTab) {
  if (n == -1 && currentTab === 3) {
    currentTab = 2;
  }
  var x = document.getElementsByClassName("tab");
  if (n > 0 && !validate_form(currentTab + n, currentTab)) return currentTab;
  x[currentTab].style.display = "none";

  currentTab = currentTab + n;

  if (currentTab == 3) {
    x[currentTab - 1].style.display = "block";
  }

  if (currentTab >= x.length) {
    return currentTab;
  } else {
    showTab(currentTab);
  }

  // hide the document imposing condition row if the attribute for imposing condition is false
  if ($("#inputImposingConditions").is(":checked")) {
    $("#row-DIC").css("display", "table-row");
  } else {
    $("#row-DIC").css("display", "none");
  }
  $("#row-CSD").css("display", "none");

  return currentTab;
};

const showTab = function (n) {
  var x = document.getElementsByClassName("tab");
  if (x[n] === undefined) {
    return;
  }
  x[n].style.display = "block";
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == x.length - 1) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  fixStepIndicator(n);
};
