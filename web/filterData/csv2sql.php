<HTML>

<HEAD>
<TITLE>CSV to SQL convertor</TITLE>
</HEAD>

<BODY>

<H2>CSV to SQL convertor</H2>

<!-- Input form begin -->

<FORM NAME="csv2sql" METHOD=POST ACTION="<?php echo $_SERVER['PHP_SELF']; ?>">
	<INPUT TYPE="HIDDEN" NAME="ref" VALUE="csv2sql">
	Insertion table:
	<BR>
	<INPUT CLASS="DEFAULT" TYPE="TEXT" NAME="table_name" VALUE="" SIZE=50>
	<BR><BR>
	CSV data: 
	<BR>
	<TEXTAREA CLASS="DEFAULT" NAME="csv_data" ROWS=30 COLS=100></TEXTAREA>
	<BR><BR>
	<INPUT CLASS="DEFAULT" TYPE=SUBMIT VALUE="     Convert to SQL query     ">
</FORM>

<!-- Input form end -->

<?php

// Parse incoming information if above form was posted
if($_POST[ref] == "csv2sql") {

	echo "<h2>SQL Query Output:</h2>";

	// Get information from form & prepare it for parsing
	$table_name = $_POST['table_name'];
	$csv_data   = $_POST['csv_data'];
	$csv_array    = explode("\n",$csv_data);
	$column_names = explode(";",$csv_array[0]);

	// Generate base query
	$base_query = "INSERT INTO $table_name (";
	$first      = true;
	foreach($column_names as $column_name)	
	{
		if(!$first)
			$base_query .= ", ";	
		$column_name = trim($column_name);
		$base_query .= "`$column_name`";
		$first = false;
	}
	$base_query .= ") ";

	// Loop through all CSV data rows and generate separate
	// INSERT queries based on base_query + the row information
	$last_data_row = count($csv_array) - 1;
	for($counter = 1; $counter < $last_data_row; $counter++)
	{
		$value_query = "VALUES (";
		$first = true;
		$data_row = explode(";",$csv_array[$counter]);
		$value_counter = 0;
		foreach($data_row as $data_value)	
		{
			if(!$first)
				$value_query .= ", ";	
			$data_value = trim($data_value);
			$value_query .= "'$data_value'";
			$first = false;
		}
		$value_query .= ")";

		// Combine generated queries to generate final query
		$query = $base_query .$value_query .";";
		echo "$query <BR>";
	}
}

?>

