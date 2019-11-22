<style>
th, td {
    padding: 10px;
}
body {
        background: #fafafa url(https://jackrugile.com/images/misc/noise-diagonal.png);
        color: #444;
        font: 100%/30px 'Helvetica Neue', helvetica, arial, sans-serif;
        text-shadow: 0 1px 0 #fff;
}

strong {
        font-weight: bold;
}

em {
        font-style: italic;
}

table {
        background: #f5f5f5;
        border-collapse: separate;
        box-shadow: inset 0 1px 0 #fff;
        font-size: 12px;
        line-height: 24px;
        margin: 30px auto;
        text-align: left;
}

th {
        background: url(https://jackrugile.com/images/misc/noise-diagonal.png), linear-gradient(#777, #444);
        border-left: 1px solid #555;
        border-right: 1px solid #777;
        border-top: 1px solid #555;
        border-bottom: 1px solid #333;
        box-shadow: inset 0 1px 0 #999;
        color: #fff;
  font-weight: bold;
        padding: 10px 15px;
        position: relative;
        text-shadow: 0 1px 0 #000;
}
th:after {
        background: linear-gradient(rgba(255,255,255,0), rgba(255,255,255,.08));
        content: '';
        display: block;
        height: 25%;
        left: 0;
        margin: 1px 0 0 0;
        position: absolute;
        top: 25%;
        width: 100%;
}

th:first-child {
        border-left: 1px solid #777;
        box-shadow: inset 1px 1px 0 #999;
}

th:last-child {
        box-shadow: inset -1px 1px 0 #999;
}

td {
        border-right: 1px solid #fff;
        border-left: 1px solid #e8e8e8;
        border-top: 1px solid #fff;
        border-bottom: 1px solid #e8e8e8;
        padding: 10px 15px;
        position: relative;
        transition: all 300ms;
}

td:first-child {
        box-shadow: inset 1px 0 0 #fff;
}

td:last-child {
        border-right: 1px solid #e8e8e8;
        box-shadow: inset -1px 0 0 #fff;
}

tr {
        background: url(https://jackrugile.com/images/misc/noise-diagonal.png);
}

tr:nth-child(odd) td {
        background: #f1f1f1 url(https://jackrugile.com/images/misc/noise-diagonal.png);
}


tr:last-of-type td {
        box-shadow: inset 0 -1px 0 #fff;
}

tr:last-of-type td:first-child {
        box-shadow: inset 1px -1px 0 #fff;
}

tr:last-of-type td:last-child {
        box-shadow: inset -1px -1px 0 #fff;
}


</style>

<h2>List of AWS VPC</h2>

<form name="refresh" action="welcome.php" method="POST">
<input type="submit" name="Main" value="Main"/>
</form>
<form name="subnet" action="subnet.php" method="POST">
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
