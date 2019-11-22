<head>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<h2>List of AWS INTERFACE</h2>

<form name="refresh" action="welcome.php" method="POST">
<input type="submit" name="Main" value="Main"/>
</form>
<form name="subnet" action="subnet.php" method="POST">
<input type="submit" name="submit" value="Submit"/>

<?php
    if (isset($_GET['subnet_id']))
    {
	//echo "test";
	$subnetid = $_GET['subnet_id'];
	//echo $subnetid;
	$command = escapeshellcmd("sudo python3 /var/www/html/list_interface.py \"$subnetid\"");
    	$output = shell_exec($command);
    }
    //$connection = new PDO('sqlite:/var/www/html/test.db');
    $connection = new SQLite3('/var/www/html/test.db');
    //if($connection){
    //    echo "Connected\n";
    //}
    $results = $connection->query('SELECT * FROM awsINTERFACE');
    echo '<table>';
    echo '<thead>';
    echo '<tr><th>INTERFACE ID</th>';
    echo '<th>INTERFACE description</th>';
    echo '<th>INTERFACE instance ID</th>';
    echo '<th></th></tr>';
    echo '</thead>';
    echo '<tbody>';
    while($row=$results->fetchArray(SQLITE3_ASSOC)){
        echo '<tr>';
	echo "<td>{$row[INTERFACE_id]}</td>";
	echo "<td>{$row[INTERFACE_desc]}</td>";
	echo "<td>{$row[INTERFACE_instanceid]}</td>";
	echo "<td><input type=\"checkbox\" name=\"interface_list[]\" value={$row[INTERFACE_id]}></td>";
        echo '</tr>';
    }
    echo '</tbody>';
    echo '</table>';
?>
</form>
