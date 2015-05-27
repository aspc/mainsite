<?php

session_set_cookie_params(0, "/", ".pomona.edu");
session_start();

$_SESSION["username"] = $argv[1];
$_SESSION["first"] = $argv[2];
$_SESSION["last"] = $argv[3];

die();

?>