function states_list(json) {
   /* 
      Get possible values for a field,
      create a list of <option> elements,
      append them to the #state <select>
   */

	
	for (i in json['data']){
		$("#state").append(
			$("<option>").attr("value", json['data'][i]).text(json['data'][i])
		);
	}
         
}
	

function results_table(json) {
	console.log(json)
    var tab = $("<table>").attr("class", "table table-hover").append(
        $("<thead>").append(
        	$("<tr>").append(
        		$("<th>").text("State"),
        		$("<th>").text("Battle Name"),
        		$("<th>").text("Casualties")

        	)
        )
    );


           
	var tbody  = $("<tbody>")	
	tab.append(tbody)

    for (i in json['data']) {
    	tbody.append(
			$("<tr>").attr("data-battle_id", json['data'][i]['battle_id']).append(
				$("<td>").text(json['data'][i]['state']),
				$("<td>").text(json['data'][i]['battle_name']),
				$("<td>").text(json['data'][i]['all_casualties'])
			).click(function(){

            get_details($(this).attr("data-battle_id"))
        	})
		)	
    }

   $("#results_col").empty().append(tab)

}


function start_search() {
   /*
      Initiates a search
   */
   // TODO: get the values of #state and #battle
	var state = $("#state").val();
	var battle = $("#battle").val();

   // TODO: do a `$.get()`, 
	$.get("/search", {"state": state, "battle": battle}, results_table);
   //   - request `/search`
   //   - pass the user params
   //   - attach results_table as the callback
}

function display_details(json) {
   /* 
      display the details of a single battle in the #details modal
   */
   	var udiv = $("<div>").append(
   		$("<p>").text(json["data"]["description"])
   	)
   	var ldiv = $("<div>").append(


    $("<table>").append(
   	$("<tr>").append(
   	$("<th>").text("Battle Name"),
	$("<td>").text(json["data"]["battle_name"])
   	),

   	$("<tr>").append(
	$("<th>").text("Start Date of Battle"),
	$("<td>").text(json["data"]["start_date"])
	),

	$("<tr>").append(
	$("<th>").text("End Date of Battle"),
	$("<td>").text(json["data"]["end_date"])
	),

	$("<tr>").append(
	$("<th>").text("State of Battle"),
	$("<td>").text(json["data"]["state"])
	),

	$("<tr>").append(
	$("<th>").text("US Commander(s)"),
	$("<td>").text(json["data"]["us_command"])
	),

	$("<tr>").append(
	$("<th>").text("Campaign"),
	$("<td>").text(json["data"]["campaign"])
	),

	$("<tr>").append(
	$("<th>").text("Location of Battle"),
	$("<td>").text(json["data"]["location"])
	),

	$("<tr>").append(
	$("<th>").text("Confederate Commander(s)"),
	$("<td>").text(json["data"]["cs_command"])
	),



	$("<tr>").append(
	$("<th>").text("Outcome"),
	$("<td>").text(json["data"]["result"])
	),

	$("<tr>").append(
	$("<th>").text("Duration of Battle (days)"),
	$("<td>").text(json["data"]["duration"])
	),

	$("<tr>").append(
	$("<th>").text("Total Number of Casualties"),
	$("<td>").text(json["data"]["all_casualties"])
	),

	$("<tr>").append(
	$("<th>").text("Northern Casualties"),
	$("<td>").text(json["data"]["us_casualties"])
	),

	$("<tr>").append(
	$("<th>").text("Southern Casualties"),
	$("<td>").text(json["data"]["cs_casualties"])
	)
	
	
    )
);
   // TODO: create an upper div for the description, lower one for a table
   
   // TODO: build the table to display your choice of record fields
   
   // TODO: set the `#detail_header` to the battle name
   $("#detail_header").text(json["data"]["battle_name"])
   // show the modal
   $("#detail_body").append(udiv,ldiv);
   $("#details").modal();

}

function get_details(id) {
   // TODO: request details json, trigger display_details
	$.get("/detail", {"battle_id": id}, display_details)
}


$(document).ready(function(){

	$.get('/states',{}, states_list);

	$("#form1").submit(function(event){
		event.preventDefault();
		start_search();
	});
   /*
      Document Ready Handler
   */

   // TODO: build the #state dropdown
   
   // TODO: hook up start_search function to the form's submit event
})