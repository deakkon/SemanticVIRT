<?php
include "dbConnect.php";
include_once 'FileCSV/DataSource.php';
$baza = new baza();

function getDirArray($Path="./",$Filter=".*",$Sorted="True")
{
        $handle=opendir($Path);
        while ($file = readdir($handle)) {
			if (is_file("$Path/$file") && eregi("$Filter", $file)) {
			                 $dirArray[] = $file;
			                }
			        }
			        closedir($handle);
			
			        if (!is_array($dirArray)) {
			                return 0;
			        }
			
			        if (strcasecmp($Sorted,"True")) {
			                shuffle($dirArray); // May not work on some systems. See php docs
			        } else {
			                sort($dirArray);
			        }			
			        return $dirArray;
}


// ------------ lixlpixel recursive PHP functions -------------
// scan_directory_recursively( directory to scan, filter )
// expects path to directory and optional an extension to filter
// of course PHP has to have the permissions to read the directory
// you specify and all files and folders inside this directory
// ------------------------------------------------------------

// to use this function to get all files and directories in an array, write:
// $filestructure = scan_directory_recursively('path/to/directory');

// to use this function to scan a directory and filter the results, write:
// $fileselection = scan_directory_recursively('directory', 'extension');

function scan_directory_recursively($directory, $filter=FALSE)
{
	$baza = new baza();
	// if the path has a slash at the end we remove it here
	if(substr($directory,-1) == '../')
	{
		$directory = substr($directory,0,-1);
	}

	// if the path is not valid or is not a directory ...
	if(!file_exists($directory) || !is_dir($directory))
	{
		echo "path not valid";
		// ... we return false and exit the function
		return FALSE;

	// ... else if the path is readable
	}elseif(is_readable($directory))
	{
		// we open the directory
		$directory_list = opendir($directory);

		// and scan through the items inside
		while (FALSE !== ($file = readdir($directory_list)))
		{
			// if the filepointer is not the current directory
			// or the parent directory
			if($file != '.' && $file != '..')
			{
				// we build the new path to scan
				$path = $directory.'/'.$file;

				// if the path is readable
				if(is_readable($path))
				{
					// we split the new path by directories
					$subdirectories = explode('/',$path);

					// if the new path is a directory
					if(is_dir($path))
					{
						// add the directory details to the file list
						$directory_tree[] = array(
							'path'    => $path,
							'name'    => end($subdirectories),
							'kind'    => 'directory',

							// we scan the new path by calling this function
							'content' => scan_directory_recursively($path, $filter));

					// if the new path is a file
					}elseif(is_file($path))
					{
						// get the file extension by taking everything after the last dot
						$extension = end(explode('.',end($subdirectories)));

						// if there is no filter set or the filter is set and matches
						if($filter === FALSE || $filter == $extension)
						{
							// add the file details to the file list
							$directory_tree[] = array(
								'path'      => $path,
								'name'      => end($subdirectories),
								'extension' => $extension,
								'size'      => filesize($path),
								'kind'      => 'file');
						}
					}
				}
			}
		}
		// close the directory
		closedir($directory_list); 

		// return file list
		//return $directory_tree;
		//print_r($directory_tree);
		//print_r(array_keys($directory_tree));

		$count = count($directory_tree);
		for ($i = 0; $i <  $count ; $i++) {
				//get UserID and SessionID
				$name = $directory_tree[$i]['name'];
				$result = explode('.',$name);
				$sesionID=$result[0];				
				$result1 = explode('_',$result[0]);
				$userID = $result1[0];
				echo "File name: $name  UID: ".$userID." SID: ".$sesionID."<br />";
				//echo "Name: $name<br />";
				
				//read through the csv file 
				$name = "C:\wamp\www\patternTest\dataUlog\\".$name;
				
				$fp = fopen($name,'r') or die("can't open file");
				print "<table>\n";
				while($csv_line = fgetcsv($fp,1024)) {
					
					if (strcmp("Date",$csv_line[0]) != 0){
						//print_r($csv_line)."<br />";
	 					$Date =$csv_line[0]; 
						$Time = $csv_line[1]; 
						$Msec = $csv_line[2]; 
						$Application = $csv_line[3]; 
						$Window = $csv_line[4]; 
						$Message= $csv_line[5]; 
						$X = $csv_line[6]; 
						$Y = $csv_line[7]; 
						$RelDist=$csv_line[8];
						$TotalDist = $csv_line[9]; 
						$Rate = $csv_line[10]; 
						$ExtraInfo = $csv_line[11];
						//$sql = "insert into ulogdata (userID, sessionID, Date, Time, Msec, Application, Window, Message, X, Y, Rel__dist_, Total_dist_, Rate, Extra_info) 
						//		values ('$userID','$sesionID','$Date','$Time','$Msec','$Application','$Window','$Message','$X','$Y','$RelDist','$TotalDist','$Rate','$ExtraInfo')";
						$sql = "insert into ulogdata (userID, sessionID, Date, Time, Msec, Application, Window, Message, X, Y, Rel__dist_, Total_dist_, Rate, Extra_info) 
								values (\"$userID\",\"$sesionID\",\"$Date\",\"$Time\",\"$Msec\",\"$Application\",\"$Window\",\"$Message\",\"$X\",\"$Y\",\"$RelDist\",\"$TotalDist\",\"$Rate\",\"$ExtraInfo\")";						
						$baza->query_mysql($sql);
						echo $userID." ".$sesionID." ".$Date." ".$Time." ".$Msec." ".$Application." ".$Window." ".$Message." ".$X." ".$Y." ".$RelDist." ".$TotalDist." ".$Rate." ".$ExtraInfo."<br />";						
					}

				    //print '<tr>';
				    /*
				    for ($i = 0, $j = count($csv_line); $i < $j; $i++) {
    						$Date =$csv_line[0]; 
							$Time = $csv_line[1]; 
							$Msec = $csv_line[2]; 
							$Application = $csv_line[3]; 
							$Window = $csv_line[4]; 
							$Message= $csv_line[5]; 
							$X = $csv_line[6]; 
							$Y = $csv_line[7]; 
							$RelDist=$csv_line[8];
							$TotalDist = $csv_line[9]; 
							$Rate = $csv_line[10]; 
							$ExtraInfo = $csv_line[11];
        					//print '<td>'.$csv_line[$i].'</td>';					 		
				    }*/
				    
				    //print "</tr>\n";
	    
				}
				//print '</table>\n';
				fclose($fp) or die("can't close file");		
				
				//echo "------------CSV MANIPULATION--------------------<br />";
				//$csv = new File_CSV_DataSource;
				//$csv->load($name);
				//var_export($csv->getHeaders());	
			}		

	// if the path is not readable ...
	}else{
		// ... we return false
		echo "mamicu ti";
		return FALSE;	
	}
}
echo "------------------------------------------------------------";
// open this directory 
$myDirectory = opendir("D:\Purdue\dragonLines\dataCollection");

// get each entry
while($entryName = readdir($myDirectory)) {
	$dirArray[] = $entryName;
}

// close directory
closedir($myDirectory);

//	count elements in array
$indexCount	= count($dirArray);
//Print ("$indexCount files<br>\n");

// sort 'em
sort($dirArray);
/*
// print 'em
print("<TABLE border=1 cellpadding=5 cellspacing=0 class=whitelinks>\n");
print("<TR><TH>Filename</TH><th>Filetype</th><th>Filesize</th></TR>\n");
// loop through the array of files and print them all
for($index=0; $index < $indexCount; $index++) {
        if (substr("$dirArray[$index]", 0, 1) != "."){ // don't list hidden files
		print("<TR><TD><a href=\"$dirArray[$index]\">$dirArray[$index]</a></td>");
		print("<td>");
		print(filetype($dirArray[$index]));
		print("</td>");
		print("<td>");
		print(filesize($dirArray[$index]));
		print("</td>");
		print("</TR>\n");
	}
}
print("</TABLE>\n");
*/
echo "------------GETTING USERID SESSIONID INFO-------------------------<br />";

scan_directory_recursively('C:\wamp\www\patternTest\dataUlog', $filter=FALSE);
	
?>
