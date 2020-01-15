<head>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<h2>List of AWS INTERFACE</h2>

<form name="refresh" action="welcome.php" method="POST">
<input type="submit" name="Main" value="Main"/>
</form>

The following interface have been configured for SLR mirroring:
<?php
    $connection = new SQLite3('/var/www/html/test.db');
    $results = $connection->query('SELECT * FROM awsINTERFACE');
    echo '<table>';
    echo '<thead>';
    echo '<tr><th>INTERFACE ID</th>';
    echo '<th>INTERFACE description</th>';
    echo '<th>INTERFACE instance ID</th>';
    echo '</tr>';
    echo '</thead>';
    echo '<tbody>';
    while($row=$results->fetchArray(SQLITE3_ASSOC)){
        echo '<tr>';
	echo "<td>{$row[INTERFACE_id]}</td>";
	echo "<td>{$row[INTERFACE_desc]}</td>";
	echo "<td>{$row[INTERFACE_instanceid]}</td>";
        echo '</tr>';
	$value_list = $value_list.",".$row[INTERFACE_id];
    }
    echo '</tbody>';
    echo '</table>';
    $command = escapeshellcmd("sudo python3 /var/www/html/create_vpc.py \"$value_list\"");
    echo $command;
    //$output = shell_exec($command);
?>
</form>
