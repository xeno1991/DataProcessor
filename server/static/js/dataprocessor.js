function _sync_pipe_api_call(data, callback){
  $.blockUI(BLOCK_SETTING);
  $.ajax({
    url: PIPE_API_URL,
    contentType: "application/json",
    type: "POST",
    data: JSON.stringify(data),
    success: function(res, st){
      if(typeof(res) == "object" && "exit_code" in res && res["exit_code"] != 0){
        alert("Server Error: " + res["message"]);
      }
      callback(res);
    },
    error: function(xhr, st, error){
      alert("Server connection failed");
    },
    complete: function(xhr, st){
      $.unblockUI();
    },
  });
}


$(function(){
    $("table.dp-projectlist").DataTable(DATATABLES_SETTING);
    $("table.dp-project").DataTable(DATATABLES_SETTING);
    enable_editable_comment();
});
