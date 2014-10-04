	// javascript code to read cars.json and create comparison.json
$(document).ready(function() {



console.log("loaded");


});

	var json_file;
	$.ajax({
		type: "GET",
		url:'cars.json',
		dataType: "json",
		success: function (response) {
			var manufacturers_to_analyze = ["Porsche","Audi","Acura","Mercedes-Benz" ];
			var manufacturers_children_index = {"Porsche": 0, "Audi": 1, "Acura": 2, "Mercedes-Benz":3};


			var l_car_nodes = [];
			var l_cars = response;
			var tree_cars = {"name": "Cars", "value":100, "children": []};

			for (var i=0; i< manufacturers_to_analyze.length; i++) {
				tree_cars["children"][tree_cars["children"].length] = {"name": manufacturers_to_analyze[i], "value":75, "children":[]};
			}

			for (var i=0; i < l_cars.length; i++) {
				var this_car = l_cars[i];
				var carname = this_car["Vehicle Name"];
				carname_split = carname.split(' ');
				var manufacturer = carname_split[0];
				this_car["value"] = 25;
				this_car["name"] = carname_split.slice(1,carname_split.length).join(' ');
				if (manufacturers_to_analyze.indexOf(manufacturer) != -1) {
					tree_cars["children"][manufacturers_children_index[manufacturer]]["children"][tree_cars["children"][manufacturers_children_index[manufacturer]]["children"].length] = l_cars[i];

				}
			}
			$(document.body).append(JSON.stringify(tree_cars));
		}
	});