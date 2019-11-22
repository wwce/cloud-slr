<head>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<h2>List of AWS INTERFACE</h2>

<form name="refresh" action="welcome.php" method="POST">
<input type="submit" name="Main" value="Main"/>
</form>
<form name="subnet" action="success.php" method="POST">
<input type="submit" name="confirm" value="confirm"/>

<?php
    if (isset($_POST['submit']))
    {
	foreach($_POST['vpc_list'] as $selected){
           $vpc_list = $vpc_list.",". $selected;
        }

        //echo "test";
        $command = escapeshellcmd("sudo python3 /var/www/html/interface_vpc.py \"$vpc_list\"");
        $output = shell_exec($command);
    }
    if (isset($_POST['confirm']))
    {
	foreach($_POST['vpc_list'] as $selected){
           $vpc_list = $vpc_list.",". $selected;
        }

        //echo "test";
        $command = escapeshellcmd("sudo python3 /var/www/html/add_tag.py \"$vpc_list\"");
        $output = shell_exec($command);
    }
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
    echo '</tr>';
    echo '</thead>';
    echo '<tbody>';
    while($row=$results->fetchArray(SQLITE3_ASSOC)){
        echo '<tr>';
	echo "<td>{$row[INTERFACE_id]}</td>";
	echo "<td>{$row[INTERFACE_desc]}</td>";
	echo "<td>{$row[INTERFACE_instanceid]}</td>";
        echo '</tr>';
    }
    echo '</tbody>';
    echo '</table>';
?>
</form>
