jQuery(document).ready(function() {
  jQuery("#feedback-dialog").dialog({
    modal: true,
    width: 500,
    position: ["center", 150],
    autoOpen: false,
    open: function() {
      log_js_action("ask-admin", "form", "show");
      jQuery("#id_url").val(window.location);
      jQuery("#feedback-form textarea").focus();
      jQuery("#feedback-form textarea").val("");
    },
    close: function(event, ui) {
      log_js_action("ask-admin", "form", "close");
    }
  });
  
  jQuery("#feedback-success").dialog({
    modal: true,
    width: 500,
    position: ["center", 150],
    autoOpen: false,
    close: function(event, ui) {
      log_js_action("ask-admin", "confirmation", "close");
    }
  });
  
  jQuery("#feedback-form textarea").keyup(function() {
    if (this.value.length == 0) {
      jQuery("#feedback-submit").attr("disabled", true);
    }
    else {
      jQuery("#feedback-submit").attr("disabled", false);
    }
  });
  
  $('#feedbackModal').modal({
      backdrop: false,
      keyboard: true,
      show: false
  }); 
  // set up event logging
  $('#feedbackModal').on('shown', function() {
      log_js_action("feedback", "form", 'feedback-open');
      jQuery("#id_url").val(window.location);
      jQuery("#feedbackModal textarea").focus();
      jQuery("#feedbackModal textarea").val("");
  });
  $('#feedbackModal').on('hidden', function() {
      log_js_action("feedback", "form", 'feedback-close');
  });
  $('#successModal').modal({
      backdrop: false,
      keyboard: true,
      show: false
  }); 
  // set up event logging
  $('#successModal').on('shown', function() {
      log_js_action("feedback", "form", 'feedback-success-open');
  });
  $('#successModal').on('hidden', function() {
      log_js_action("feedback", "form", 'feedback-success-close');
  });
  
  jQuery("#header-feedback").click(function() {
//    jQuery("#feedback-dialog").dialog("open");
	  $('#feedbackModal').modal('show');
  });
  
  jQuery("#feedback-submit").click(function() {
    if(!jQuery(this).attr("disabled")) {
      jQuery(this).attr("disabled", true);
      // alert(this.form.action);
      jQuery("#feedback-spinner").show();
      
      $.post(this.form.action, jQuery("#feedback-form").serialize(), function(data) {
//        jQuery("#feedback-dialog").dialog("close");
          jQuery("#feedback-spinner").hide();
    	  $('#feedbackModal').modal('hide');
    	  $('#feedbackModal textarea').val("");
    	  $('#successModal').modal('show');
//        jQuery("#feedback-success").dialog("open");
      });
    }
    
    return false;
  });
  
  jQuery("#feedback-success button").click(function() {
//    jQuery("#feedback-success").dialog("close");
  })
  jQuery("#header-feedback").removeAttr("disabled");
});