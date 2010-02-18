 $(document).ready(function(){
   
   $(".submit").click(function(event){
     $(".period").each(function(i){
		start = $("#" + $(this).attr("id") + "_start");
		start.removeAttr("disabled");
		end = $("#" + $(this).attr("id") + "_end");
		end.removeAttr("disabled");
     });
   }); 
   
   
   $(".group_by").click(function(event){
     $("#show_details_check").attr("checked", "checked");
     
   }); 
   
   
   // Transforms a textbox whose id is given into a datetime picker				
   initDateTime = function(id){
	   jQuery(id).dynDateTime({
			showsTime: true,
			ifFormat: "%d/%m/%Y %H:%M",
			daFormat: "%l;%M %p, %e %m,  %Y",
			align: "BL",
			electric: true
		});
	}
	
   // Transforms all textboxes with class "jq_datetime" into datetimepickers
   $(".jq_datetime").each(function(i){
						initDateTime(this);
					});
   
   $(".period").each(function(i){
   		$(this).change(function(event){
			var value = $(this).val();
			
			if (value == "(custom)")
			{
				$("#" + $(this).attr("id") + "_start").removeAttr("disabled");
				$("#" + $(this).attr("id") + "_end").removeAttr("disabled");
			} else 
			{	
				$("#" + $(this).attr("id") + "_start").attr("disabled", "True");
				$("#" + $(this).attr("id") + "_end").attr("disabled", "True");
				
				var now = new Date();
				var startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 7, 0, 0, 0);
				var endDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 7, 0, 0, 0);
				
				if (value == "This week"){
					if (now.getDay() == 0){
						startDate.addDays(-6);
					} else 
					{
						startDate.addDays(-1 * (now.getDay() - 1));
						endDate.addDays(7 - now.getDay());
					}
				} else 
				if (value == "Previous week"){
					if (now.getDay() == 0){
						startDate.addDays(-13);
						endDate.addDays(-7);
					} else 
					{
						startDate.addDays(-1 * (now.getDay() - 1) - 7);
						endDate.addDays(-1 * now.getDay());
					}
				} else 
				if (value == "This month"){
					startDate.setDate(1);
					endDate.setDate(1);
					endDate.addMonths(1);
				} else 
				if (value == "Previous month"){
					startDate.setDate(1);
					startDate.addMonths(-1);
					endDate.setDate(1);
				}
					
				$("#" + $(this).attr("id") + "_start").attr("value", startDate.friendlyString());
				$("#" + $(this).attr("id") + "_end").attr("value", endDate.friendlyString());
			}
		});
		
		start = $("#" + $(this).attr("id") + "_start");
		end = $("#" + $(this).attr("id") + "_end");
		
		if (this.selectedIndex != 0)
		{
			start.attr("disabled", "True");
			end.attr("disabled", "True");
		}
			
     });
     
     $(".list_filter").each(function(i){
   		$(this).dropdownchecklist({ firstItemChecksAll: true, width: 120, maxDropHeight: 150 });
     });
 });

 
 /*
  * DATETIME functions
  */
 Date.prototype.addDays = function(days) {
	this.setDate(this.getDate() + days);
	return this;
}

Date.prototype.addMonths = function(months) {
	this.setMonth(this.getMonth() + months, this.getDate());
	return this;
}

leadzero = function(str){
	if (str.length == 1)
		return "0" + str;
	return str;
}

Date.prototype.friendlyString = function(){
	var str = leadzero("" + this.getDate()) + "/" + leadzero("" + (this.getMonth() + 1)) + "/" + this.getFullYear();
	str = str + " " + leadzero("" + this.getHours()) + ":" + leadzero("" + this.getMinutes());
	
	return str;
}