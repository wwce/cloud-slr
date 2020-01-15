<head>
<link rel="stylesheet" type="text/css" href="style.css">
</head>


<h2>List of AWS subnet</h2>

<form name="refresh" action="welcome.php" method="POST">
<input type="submit" name="Main" value="Main"/>
</form>
<form name="subnet" action="confirm.php" method="POST">
<input type="submit" name="submit" value="Submit"/>

<?php
    if (isset($_GET['vpc_id']))
    {
	//echo "test";
	$vpcid = $_GET['vpc_id'];
	$command = escapeshellcmd("sudo python3 /var/www/html/list_subnet.py \"$vpcid\"");
    	$output = shell_exec($command);
    }
    //$connection = new PDO('sqlite:/var/www/html/test.db');
    $connection = new SQLite3('/var/www/html/test.db');
    //if($connection){
    //    echo "Connected\n";
    //}
    $results = $connection->query('SELECT * FROM awsSUBNET');
    echo '<table>';
    echo '<thead>';
    echo '<tr><th>SUBNET ID</th>';
    echo '<th>SUBNET description</th>';
    echo '<th>SLR on all existing interface</th></tr>';
    echo '</thead>';
    echo '<tbody>';
    while($row=$results->fetchArray(SQLITE3_ASSOC)){
        echo '<tr>';
	echo "<td><a href=interface.php?subnet_id=",$row[SUBNET_id] ,">{$row[SUBNET_id]}</a></td>";
	echo "<td>{$row[SUBNET_desc]}</td>";
	echo "<td><input type=\"checkbox\" name=\"subnet_list[]\" value={$row[SUBNET_id]}></td>";
        echo '</tr>';
    }
    echo '</tbody>';
    echo '</table>';
?>
</form>
