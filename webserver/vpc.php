
<head>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<h1>List of AWS VPC</h1>

<form name="refresh" action="welcome.php" method="POST">
<input type="submit" name="Main" value="Main"/>
</form>
<form name="subnet" action="confirm.php" method="POST">
<input type="submit" name="submit" value="Submit"/>

<?php
    if (isset($_POST['vpc']))
    {
	//echo "test";
	$command = escapeshellcmd('sudo python3 /var/www/html/list_vpc.py');
    	$output = shell_exec($command);
    }
    //$connection = new PDO('sqlite:/var/www/html/test.db');
    $connection = new SQLite3('/var/www/html/test.db');
    //if($connection){
    //    echo "Connected\n";
    //}
    $results = $connection->query('SELECT * FROM awsVPC');
    echo '<table>';
    echo '<thead>';
    echo '<tr><th>VPC ID</th>';
    echo '<th>VPC description</th>';
    echo '<th>SLR on all existing interface</th></tr>';
    echo '</thead>';
    echo '<tbody>';
    while($row=$results->fetchArray(SQLITE3_ASSOC)){
        echo '<tr>';
	echo "<td><a href=subnet.php?vpc_id=",$row[VPC_id] ,">{$row[VPC_id]}</a></td>";
	echo "<td>{$row[VPC_desc]}</td>";
	echo "<td><input type=\"checkbox\" name=\"vpc_list[]\" value={$row[VPC_id]}></td>";
        echo '</tr>';
    }
    echo '</tbody>';
    echo '</table>';
?>
</form>
