#!/bin/awk -f
BEGIN { }
{	if($1 == "+"){
		print($2,$6) > "traces/"
		print($2,$9) > "traces/"
	}else if($1 == "-"){
		print($2,$6) > "traces/"
		print($2,$9) > "traces/"
	}else if($1 == "d"){
		print($2,$6) > "traces/"
		print($2,$9) > "traces/"
	}
}
END {  }