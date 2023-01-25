/* javascript for managing modal forms*/

 $(function () {
    // Create synchronous
          function createContactSyncModalForm() {
            $("#create-contact-sync").modalForm({
                formURL: "{% url 'sales:contact_new' %}",
                modalID: "#create-modal"
            });
          }
          createContactSyncModalForm();

    // Create book asynchronous button
        // message  -----  WIP TODO remove was abandoned
        var asyncSuccessMessageCreate = [
            "<div ",
            "style='position:fixed;top:0;z-index:10000;width:100%;border-radius:0;' ",
            "class='alert alert-icon alert-success alert-dismissible fade show mb-0' role='alert'>",
            "Success: Contact was created.",
            "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>",
            "<span aria-hidden='true'>&times;</span>",
            "</button>",
            "</div>",
            "<script>",
            "$('.alert').fadeTo(2000, 500).slideUp(500, function () {$('.alert').slideUp(500).remove();});",
            "<\/script>"
          ].join("");

            /*var pathStructure = window.location.protocol + '//' + window.location.host + "/sales";
            //use this to get the full url making the request it contains the pk of the policy needed to supply the filtered data
            */
            var pathStructure = window.location.protocol + '//' + window.location.host + "/sales";
            var create_location = window.location.href;
            var c_Array = create_location.split('/');
            var c_len = c_Array.length, j;
            for (j=0; j <c_len; j++)
                c_Array[j] && c_Array.push(c_Array[j]);

            c_Array.splice(0, c_len); // remove the empty values then use the last one that is the pk
            var c_last_element = c_Array.pop();
            var c_new_url = pathStructure + "/contact_data/" + c_last_element + "/";
            console.log(c_new_url);

          // modal form  -----   WIP 14/10, TODO remove was abandoned
          function createBookAsyncModalForm() {
            $("#create-contact-async").modalForm({
                formURL: "{% url 'sales:contact_new' %}",
                modalID: "#create-modal",
                asyncUpdate: true,
                asyncSettings: {
                  closeOnSubmit: true,
                  successMessage: asyncSuccessMessageCreate,
                  dataUrl: '',   // DT updated
                  dataElementId: "#contacts-table",
                  dataKey: "table",
                  addModalFormFunction: reinstantiateModalForms
                }
            });
          }
          createBookAsyncModalForm();

      // Update contact asynchronous button
          // message
              var asyncSuccessMessageUpdate = [
                "<div ",
                "style='position:fixed;top:0;z-index:10000;width:100%;border-radius:0;' ",
                "class='alert alert-icon alert-success alert-dismissible fade show mb-0' role='alert'>",
                "Success: Contact was updated.",
                "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>",
                "<span aria-hidden='true'>&times;</span>",
                "</button>",
                "</div>",
                "<script>",
                "$('.alert').fadeTo(2000, 500).slideUp(500, function () {$('.alert').slideUp(500).remove();});",
                "<\/script>"
              ].join("");

            var pathStructure = window.location.protocol + '//' + window.location.host + "/sales";
            //use this to get the full url making the request it contains the pk of the policy needed to supply the filtered data
            var fullLoc = window.location.href;
            console.log(fullLoc);
            var pathArray = fullLoc.split('/');
            var len = pathArray.length, i;
            for (i=0; i <len; i++)
                pathArray[i] && pathArray.push(pathArray[i]);

            pathArray.splice(0, len); // remove the empty values then use the last one that is the pk
            var last_element = pathArray.pop();
            var new_url = pathStructure + "/contact_data/" + last_element + "/";
            //console.log(new_url);

          // modal form
              function updateContactModalForm() {
                $(".update-contact").each(function () {
                  $(this).modalForm({
                    formURL: $(this).data("form-url"),
                    asyncUpdate: true,
                    asyncSettings: {
                      closeOnSubmit: true,
                      successMessage: asyncSuccessMessageUpdate,
                      dataUrl: new_url,   //
                      dataElementId: "#contacts-table",  //
                      dataKey: "table",
                      addModalFormFunction: reinstantiateModalForms
                    }
                  });
                });
              }
          updateContactModalForm(); //

          // Delete book buttons - formURL is retrieved from the data of the element
              function deleteContactModalForm() {
                $(".delete-contact").each(function () {
                    $(this).modalForm({formURL: $(this).data("form-url"), isDeleteForm: true});
                });
              }
              deleteContactModalForm();   //

          // Read contact buttons
              function readContactModalForm() {
                $(".read-contact").each(function () {   //this is the class assigned to each of the buttons
                    $(this).modalForm({formURL: $(this).data("form-url")});
                });
              }
              readContactModalForm();  //

          function reinstantiateModalForms() {
            //createBookAsyncModalForm();
            createContactSyncModalForm();
            readContactModalForm();
            updateContactModalForm();
            deleteContactModalForm();
          }

          // Filter books button  ----- TODO remove
              $("#filter-book").each(function () {
                  $(this).modalForm({formURL: $(this).data("form-url")});
              });

          // Hide message  -----
              $(".alert").fadeTo(2000, 500).slideUp(500, function () {
                  $(".alert").slideUp(500);
              });

  $("#js-create-contact").click(function () {
    $.ajax({
      url: '/sales/contact_policy_create/',  // will need to make this dynamic removed the policy fk 4/
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#my_ajax_modal").modal("show");
      },
      success: function (data) {
        $("#my_ajax_modal .modal-content").html(data.html_form);
      }
    });
  });

//js-book-create-form refers to the form class of the modal form

  $("#my_ajax_modal").on("submit", ".js-contact-create-form", function () {
      var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#contacts_table_body").empty().html(data.html_contact_list);
          $("#my_ajax_modal").modal("hide");
          //alert("Contact created!");  // <-- This is just a placeholder for now for testing
        }
        else {
          $("#my_ajax_modal .modal-content").html(data.html_form);
        }
      }
    });
    return false;  //this to cancel the full post request
  });

    // below is to create a contact on the specific policy
    $("#js-create-contact-polx").click(function () {
        var pol_id = $("#pol_id").html();
        //alert("policy" + pol_id);
        var target_url = '/sales/contact_add/' + pol_id + '/';
    $.ajax({
      url: target_url,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#my_ajax_modal").modal("show");
      },
      success: function (data) {
        $("#my_ajax_modal .modal-content").html(data.html_form);
      }
    });
  });


//add datepicker class = dateinput  #id_inception__lt
    $(".dateinput").datepicker({
            dateFormat: "yy-mm-dd"
            });

    $('#clear_button').click(function(){
        var inputs = document.getElementsByTagName('input');
            for (var index = 0; index < inputs.length; ++index) {
                if (inputs[index].value != 'Clear Filters') {
                    inputs[index].value = '';
                };
            };
        document.forms['filter_form'].submit();
    });

      });
