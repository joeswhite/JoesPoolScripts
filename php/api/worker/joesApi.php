<?php
/*
	Joe's Pool PHP API parser class
	Copyright 2014 Joe White (https://freicoin.us)
	joe@freicoin.us

	Donations (FRC): 1KY3h7vTcTTA1m1bQVrmthoKwf9YEAWyvi

	Version 0.001 Pre-Alpha

	License AGPL 3.0 
*/
/* CHANGE THESE SETTINGS */

$apiKey = "enterYourKeyHere"; // This is your API KEY found in your account details section



/* DO NOT CHANGE ANY CODE BELOW */
$version = "0.001 Pre-Alpha";
class joesApi {

	/* source https://github.com/ryanuber/projects/blob/master/PHP/JSON/json_split_objects.php */

	/**
	 * json_split_objects - Return an array of many JSON objects
	 *
	 * In some applications (such as PHPUnit, or salt), JSON output is presented as multiple
	 * objects, which you cannot simply pass in to json_decode(). This function will split
	 * the JSON objects apart and return them as an array of strings, one object per indice.
	 *
	 * @param string $json  The JSON data to parse
	 *
	 * @return array
	 */
	function json_split_objects($json)
	{
	    $q = FALSE;
	    $len = strlen($json);
	    for($l=$c=$i=0;$i<$len;$i++)
	    {   
	     	$json[$i] == '"' && ($i>0?$json[$i-1]:'') != '\\' && $q = !$q;
	        if(!$q && in_array($json[$i], array(" ", "\r", "\n", "\t"))){continue;}
	        in_array($json[$i], array('{', '[')) && !$q && $l++;
	        in_array($json[$i], array('}', ']')) && !$q && $l--;
	        (isset($objects[$c]) && $objects[$c] .= $json[$i]) || $objects[$c] = $json[$i];
	        $c += ($l == 0);
	    }   
	    return $objects;
	}

	function workerInfo($apiKey) {
		/* This variable gets us the latestworker stats */
		$joes = file_get_contents('http://freicoin.us/bhutsrgtefyhgtr/newpool/api.php?mode=json&api_key='.$apiKey);

		/* This splits and decodes the json string so we can use it */
		foreach ($this->json_split_objects($joes) as $key => $value) {
			$joe = json_decode($value, true);
			$worker[$key]["name"]         = $joe["name"];
			$worker[$key]["alive"]        = $joe["alive"];
			$worker[$key]["hashrate"]     = $joe["hashrate"];
			$worker[$key]["mandiff"]      = $joe["mandiff"];
			$worker[$key]["mandiffvalue"] = $joe["mandiffvalue"];
		}
		return $worker;
	}

}


/* Example use of function */

/* construct the function */
$joesCall = new joesApi();
$joesStats = $joesCall->workerInfo($apiKey);

/* announce the name of the script */
echo "Joe's Pool (FreiCoin.US) Worker Hashrate API Example AGPL 3.0 Licensed";
echo "\n";

/* loop through ech of the workers stats and echo. Change \n to \n</br> to display on html with new lines */
foreach ($joesStats as $workerStats) {

	/* parse the array returned via json for information needed */
	$name = $workerStats['name'];
	$alive = $workerStats['alive'];
	$hashrate = $workerStats['hashrate'];
	$mandiff = $workerStats['mandiff'];
	$mandiffvalue = $workerStats['mandiffvalue'];

	/* announce info we have */
	echo "Worker: ".$name;
	echo "\n";
	echo "Alive: ";

	/* if it's alive announce the info we have, otherwise say no and move along */
	if ($alive == "1") {
		echo "Yes";
		echo "\n";
	        echo "Hashrate: ".$hashrate;
		echo "\n";
		echo "Mandiff: ";
		/* if mandiff (user defined difficulty) is enabled, announce. otherwise say no and go on */
		if ($mandiff == "1") {
			echo "Yes";
			echo "\n";
			echo "Mandiff Value: ".$mandiffvalue;
		} else {
			echo "No";
		}
	} else {
		echo "No";
		echo "\n";
	}
}


