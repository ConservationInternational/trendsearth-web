$(document).ready(function () {
  $("#workflow").select2({ placeholder: "Workflow", allowClear: true });
  $("#task").select2({ placeholder: "Task", allowClear: true });
  $("#status").select2({ placeholder: "Status", allowClear: true });
  $("#holder").select2({ placeholder: "Holder", allowClear: true });

  $("#task_tbl").DataTable({
    paging: true,
    ordering: true,
    info: true,
    language: {
      infoEmpty: "No records available - Got it?",
    },
  });
  var users_tbl = $("#users_tbl").DataTable({
    paging: true,
    ordering: true,
    info: true,
    language: {
      infoEmpty: "No users available!",
    },
  });

  var roles_tbl = $("#roles_tbl").DataTable({
    paging: true,
    ordering: true,
    info: true,
  });

  const events = function () {
    $(".item").on("click", function () {
      /** set a toolbar item active when clicked*/
      $(".item").removeClass("active");
      $(this).addClass("active");
    });

    $("#inputRegion, #inputTypeRelevantAuthority").change(function () {
      /**
       * Append the relevant authority name options based on the selection of region and relevant authority type
       */
      const url = $("#lodgementForm1").attr("data-rel_auth-url");
      const region_id = $("#inputRegion").val();
      const rel_auth_type = $("#inputTypeRelevantAuthority").val();
      if (region_id == "" || rel_auth_type == "") {
        return;
      }
      $.ajax({
        url: url,
        data: {
          type_relevant_auth: rel_auth_type,
          region: region_id,
        },
        success: function (data) {
          $("#inputNameRelevantAuthority").html(data);
        },
      });
    });

    $("#inputNameRelevantAuthority").change(function () {
      /**
       * Append the registration division options on a change to the name of the relevant authority
       */
      const url = $("#lodgementForm1").attr("data-reg_div-url");
      const rel_auth_id = $(this).val();
      if (rel_auth_id == "") {
        return;
      }
      $.ajax({
        url: url,
        data: {
          rel_auth_id: rel_auth_id,
        },
        success: function (data) {
          $("#inputRegistrationDivision").html(data);
        },
      });
    });

    $("#inputRegistrationDivision").change(function () {
      /**
       * Get the scheme number on the change of the registration division
       */
      $.ajax({
        url: "/ajax/get_scheme_number",
        data: {
          rel_auth_id: $("#inputNameRelevantAuthority").val(),
        },
        success: function (response) {
          $("#inputSchemeNumber").val(response.code);
        },
      });
    });

    $("#users_tbl tbody").on("click", "tr", function () {
      /**
       * Listen the row click event on the users table. Enable the buttons on a click
       */
      var id = this.id;
      $("#users_tbl tbody tr").removeClass("selected");
      $("#btn_show_user_summary").removeClass("disabled");
      $("#btn_edit_user").removeClass("disabled");
      $("#btn_disable_user").removeClass("disabled");
      $("#btn_delete_user").removeClass("disabled");
      $(this).toggleClass("selected");
    });

    $("#task_tbl tbody").on("click", "tr", function () {
      /**
       * Listen the row click event on the tasks table. Enable the buttons on a click
       */
      var id = this.id;
      $("#task_tbl tbody tr").removeClass("selected");
      $("#btn_edit_scheme").removeClass("disabled");
      $("#btn_delete_scheme").removeClass("disabled");
      $(this).toggleClass("selected");
    });

    $("#btn_submit_comment").on("click", function () {
      /**
       * Submit new comments to the database
       */
      $.ajax({
        url: "/ajax/post_comment",
        data: {
          comment: $("#inputComment").val(),
        },
        method: "post",
        success: function (response) {
          console.log(response);
        },
      });
    });
  };

  events();

  const format_holders = function (d) {
    /***
     * Create a component for displaying holders information whenever the more icon is clicked
     */
    return `<div class="block border">
              <div class="block-content">
                <div class="pull-r-l pull-t push">
                  <div class="table-responsive">
                    <table class="table table-hover  bg-gray-lighter border-b">
                      <tbody>
                        <tr>
                          <td class="border-r" style="width: 15%;"><b>Date of Birth:</b></td>
                          <td>${d.date_of_birth}</td>
                          <td class="border-r" style="width: 15%;"><b>Marital Status:</b></td>
                          <td>${d.marital_status}</td>
                        </tr>
                        <tr>
                          <td class="border-r" style="width: 15%;"><b>Juristic Person Name:</b></td>
                          <td>${d.juristic_person_name}</td>
                          <td class="border-r" style="width: 15%;"><b>Juristic Person Number:</b></td>
                          <td>${d.juristic_person_number}</td>
                        </tr>
                        <tr>
                          <td class="border-r" style="width: 15%;"><b>Nature of Marriage:</b></td>
                          <td>${d.nature_of_marriage}</td>
                          <td class="border-r" style="width: 15%;"><b>Disability Status:</b></td>
                         <td>${d.disability_status}</td>
                        </tr>
                        <tr>
                          <td class="border-r" style="width: 15%;"><b>Occupation:</b></td>
                          <td>${d.occupation}</td>
                          <td class="border-r" style="width: 15%;"><b>Income Level:</b></td>
                          <td>${d.income_level}</td>
                        </tr>
                        <tr>
                          <td class="border-r" style="width: 15%;"><b>Spouse Name:</b></td>
                          <td>${d.spouse_name}</td>
                          <td class="border-r" style="width: 15%;"><b>Spouse Gender:</b></td>
                          <td>${d.spouse_gender}</td>
                        </tr>
                        <tr>
                          <td class="border-r" style="width: 15%;"><b>Spouse Identifier:</b></td>
                          <td>${d.spouse_identifier}</td>
                          <td class="border-r" style="width: 15%;"><b>Spouse Date of Birth:</b></td>
                          <td>${d.spouse_date_of_birth}</td>
                        </tr>
                        <tr>
                          <td class="border-r" style="width: 15%;"><b>Dependants:</b></td>
                          <td>${d.other_dependants}</td>
                          <td class="border-r" style="width: 15%;"><b>Transfer Contract Date:</b></td>
                          <td>${d.transfer_contract_date}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
    </div>`;
  };
});

const populate_holders_tbl = function () {
  var dt = $("#holders_tbl").DataTable({
    paging: true,
    ordering: true,
    columns: [
      {
        class: "details-control",
        orderable: false,
        data: null,
        defaultContent: "",
      },
      { data: "index" },
      { data: "name" },
      { data: "identifier" },
      { data: "gender" },
      { data: "transfer_contract_number" },
      { data: "plot_number" },
      { data: "plot_use" },
      { data: "url" },
      { data: "date_of_birth" },
      { data: "marital_status" },
      { data: "juristic_person_name" },
      { data: "juristic_person_number" },
      { data: "nature_of_marriage" },
      { data: "disability_status" },
      { data: "occupation" },
      { data: "income_level" },
      { data: "spouse_name" },
      { data: "spouse_gender" },
      { data: "spouse_identifier" },
      { data: "spouse_date_of_birth" },
      { data: "other_dependants" },
      { data: "transfer_contract_date" },
    ],
  });
  var detailRows = [];

  $("#holders_tbl tbody").on("click", "tr td.details-control", function () {
    var tr = $(this).closest("tr");
    var row = dt.row(tr);
    var idx = $.inArray(tr.attr("id"), detailRows);

    if (row.child.isShown()) {
      tr.removeClass("details");
      row.child.hide();

      // Remove from the 'open' array
      detailRows.splice(idx, 1);
    } else {
      tr.addClass("details");
      row.child(format_holders(row.data())).show();

      // Add to the 'open' array
      if (idx === -1) {
        detailRows.push(tr.attr("id"));
      }
    }
  });

  dt.on("draw", function () {
    $.each(detailRows, function (i, id) {
      $("#" + id + " td.details-control").trigger("click");
    });
  });
};
